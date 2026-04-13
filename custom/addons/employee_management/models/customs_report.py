from odoo import models

class CustomsReport(models.AbstractModel):
    _name = 'report.employee_management.report_customs'
    _description = 'Customs Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.landed.cost'].browse(docids)

        lines = []

        for doc in docs:

            for val in doc.valuation_adjustment_lines:

                product = val.product_id

                # ✅ Purchase Cost (EUR from PO)
                cost_price_eur = val.former_cost or 0.0

                # ✅ Freight (AED from landed cost)
                freight_aed = val.additional_landed_cost or 0.0

                # ✅ Currency conversion
                eur_currency = self.env.ref('base.EUR')
                aed_currency = self.env.company.currency_id

                # Convert freight AED → EUR
                freight_eur = aed_currency._convert(
                    freight_aed,
                    eur_currency,
                    self.env.company,
                    doc.date
                )

                # Convert cost EUR → AED
                cost_price_aed = eur_currency._convert(
                    cost_price_eur,
                    aed_currency,
                    self.env.company,
                    doc.date
                )

                # ✅ Exemption (ONLY on freight)
                exemption_percent = getattr(product, 'exemption_percent', 0.0)

                exemption_aed = freight_aed * (exemption_percent / 100)
                exemption_eur = freight_eur * (exemption_percent / 100)

                # ✅ Totals
                total_eur = cost_price_eur + freight_eur - exemption_eur
                total_aed = cost_price_aed + freight_aed - exemption_aed

                lines.append({
                    'product': product.name,
                    'hs_code': product.hs_code or '',
                    'country': product.country_of_origin or '',

                    'cost_price_eur': cost_price_eur,
                    'cost_price_aed': cost_price_aed,

                    'freight_eur': freight_eur,
                    'freight_aed': freight_aed,

                    'exemption_eur': exemption_eur,
                    'exemption_aed': exemption_aed,

                    'total_eur': total_eur,
                    'total_aed': total_aed,
                })

        return {
            'docs': docs,
            'lines': lines,
        }