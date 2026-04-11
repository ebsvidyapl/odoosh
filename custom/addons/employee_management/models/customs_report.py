from odoo import models


class CustomsReport(models.AbstractModel):
    _name = 'report.employee_management.report_customs'
    _description = 'Customs Exemption Report'

    def _get_report_values(self, docids, data=None):

        docs = self.env['stock.landed.cost'].browse(docids)

        lines = []

        for cost in docs:
            for line in cost.valuation_adjustment_lines:

                # ✅ Get actual product
                if line.move_id:
                    product = line.move_id.product_id
                else:
                    product = line.product_id

                if not product:
                    continue

                tmpl = product.product_tmpl_id

                hs_code = (tmpl.hs_code or '').strip().upper()
                country = tmpl.country_of_origin_id

                landed_cost = line.additional_landed_cost or 0.0

                # ✅ Find rule
                rule = self.env['customs.exemption.rule'].search([
                    ('hs_code', '=', hs_code),
                    ('country_id', '=', country.id),
                    ('active', '=', True)
                ], limit=1)

                # ✅ APPLY EXEMPTION ONLY ON LANDED COST
                if rule:
                    if rule.exemption_type == 'full':
                        exemption = landed_cost

                    elif rule.exemption_type == 'partial':
                        exemption = landed_cost * (rule.exemption_percentage / 100.0)
                else:
                    exemption = 0.0

                # ✅ ROUND VALUES
                landed_cost = round(landed_cost, 2)
                exemption = round(exemption, 2)

                lines.append({
                    'cost_name': cost.name,
                    'product': product.name,
                    'hs_code': hs_code,
                    'country': country.name if country else '',
                    'landed_cost': landed_cost,
                    'exemption': exemption,
                })

        return {
            'docs': docs,
            'lines': lines,
        }