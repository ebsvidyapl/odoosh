from odoo import models, fields


class CustomsReport(models.AbstractModel):
    _name = 'report.employee_management.report_customs'
    _description = 'Customs Exemption Report'

    def _get_report_values(self, docids, data=None):

        docs = self.env['stock.landed.cost'].browse(docids)

        lines = []

        company = self.env.company
        company_currency = company.currency_id

        # ✅ Get EUR currency
        eur_currency = self.env['res.currency'].search([('name', '=', 'EUR')], limit=1)

        for cost in docs:
            for line in cost.valuation_adjustment_lines:

                # ✅ Product
                product = line.move_id.product_id if line.move_id else line.product_id
                if not product:
                    continue

                tmpl = product.product_tmpl_id

                # ✅ Basic Info
                hs_code = (tmpl.hs_code or '').strip()
                country = tmpl.country_of_origin_id

                # ✅ COST (AED)
                cost_price_aed = line.former_cost or 0.0

                # ✅ FREIGHT (AED)
                freight_aed = line.cost_line_id.price_unit or 0.0

                # ✅ FINAL COST AFTER EXEMPTION (AED)
                final_aed = line.additional_landed_cost or 0.0

                # ✅ EXEMPTION
                exemption = freight_aed - final_aed

                # ✅ TOTAL
                total_aed = cost_price_aed + final_aed

                # ✅ DATE FOR CONVERSION
                date = fields.Date.today()

                # ✅ CONVERT AED → EUR
                cost_price_eur = company_currency._convert(cost_price_aed, eur_currency, company, date)
                freight_eur = company_currency._convert(freight_aed, eur_currency, company, date)
                final_eur = company_currency._convert(final_aed, eur_currency, company, date)
                total_eur = company_currency._convert(total_aed, eur_currency, company, date)

                # ✅ ROUND
                lines.append({
                    'cost_name': cost.name,
                    'product': product.name,
                    'hs_code': hs_code,
                    'country': country.name if country else '',

                    # AED
                    'cost_price_aed': round(cost_price_aed, 2),
                    'freight_aed': round(freight_aed, 2),
                    'final_aed': round(final_aed, 2),
                    'total_aed': round(total_aed, 2),

                    # EUR
                    'cost_price_eur': round(cost_price_eur, 2),
                    'freight_eur': round(freight_eur, 2),
                    'final_eur': round(final_eur, 2),
                    'total_eur': round(total_eur, 2),

                    # Exemption
                    'exemption': round(exemption, 2),
                })

        return {
            'docs': docs,
            'lines': lines,
        }