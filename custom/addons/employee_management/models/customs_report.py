from odoo import models

class CustomsReport(models.AbstractModel):
    _name = 'report.employee_management.report_customs'
    _description = 'Customs Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.landed.cost'].browse(docids)

        eur_currency = self.env.ref('base.EUR')
        company_currency = self.env.company.currency_id

        report_lines = []

        for doc in docs:
            for line in doc.valuation_adjustment_lines:

                product = line.product_id

                if not product:
                    continue

                # ✅ ORIGINAL PURCHASE COST (DO NOT CONVERT AGAIN)
                purchase_line = line.move_id.purchase_line_id if line.move_id else False

                if purchase_line:
                    cost_eur = purchase_line.price_unit  # already EUR
                    purchase_currency = purchase_line.order_id.currency_id
                else:
                    cost_eur = 0.0
                    purchase_currency = eur_currency

                # ✅ Convert purchase → AED only once
                cost_aed = purchase_currency._convert(
                    cost_eur,
                    company_currency,
                    doc.company_id,
                    doc.date
                )

                # ✅ FREIGHT (comes in AED in landed cost)
                freight_aed = line.additional_landed_cost

                # Convert AED → EUR
                freight_eur = company_currency._convert(
                    freight_aed,
                    eur_currency,
                    doc.company_id,
                    doc.date
                )

                # ✅ EXEMPTION (ONLY on freight)
                exemption = 0.0

                hs_code = (product.product_tmpl_id.hs_code or '').replace('.', '').strip()
                country_id = product.country_of_origin_id.id

                rule = self.env['customs.exemption.rule'].search([
                    ('hs_code', '=', hs_code),
                    ('country_id', '=', country_id),
                    ('active', '=', True)
                ], limit=1)

                if rule:
                    if rule.exemption_type == 'full':
                        exemption = freight_aed
                    elif rule.exemption_type == 'partial':
                        exemption = freight_aed * (rule.exemption_percentage / 100.0)

                # Convert exemption to EUR
                exemption_eur = company_currency._convert(
                    exemption,
                    eur_currency,
                    doc.company_id,
                    doc.date
                )

                # ✅ TOTAL
                total_aed = cost_aed + (freight_aed - exemption)
                total_eur = cost_eur + (freight_eur - exemption_eur)

                report_lines.append({
                    'product': product.name,
                    'hs_code': product.product_tmpl_id.hs_code,
                    'country': product.country_of_origin_id.name,
                    'cost_eur': cost_eur,
                    'cost_aed': cost_aed,
                    'freight_eur': freight_eur,
                    'freight_aed': freight_aed,
                    'exemption_aed': exemption,
                    'exemption_eur': exemption_eur,
                    'total_eur': total_eur,
                    'total_aed': total_aed,
                })

        return {
            'docs': docs,
            'lines': report_lines,
        }