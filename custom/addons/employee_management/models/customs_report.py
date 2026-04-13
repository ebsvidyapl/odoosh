from odoo import models


class CustomsReport(models.AbstractModel):
    _name = 'report.employee_management.report_customs'
    _description = 'Customs Exemption Report'

    def _get_report_values(self, docids, data=None):

        docs = self.env['stock.landed.cost'].browse(docids)

        lines = []

        for cost in docs:
            for line in cost.valuation_adjustment_lines:

                # ✅ Get correct product
                if line.move_id:
                    product = line.move_id.product_id
                else:
                    product = line.product_id

                if not product:
                    continue

                tmpl = product.product_tmpl_id

                hs_code = (tmpl.hs_code or '').strip()
                country = tmpl.country_of_origin_id
                cost_price = product.standard_price or 0.0
                # ✅ ORIGINAL COST (before exemption)
                original_cost = line.cost_line_id.price_unit or 0.0

                # ✅ FINAL COST (after exemption applied)
                final_cost = line.additional_landed_cost or 0.0

                # ✅ EXEMPTION CALCULATION
                exemption = original_cost - final_cost

                # ✅ ROUND VALUES (important)
                original_cost = round(original_cost, 2)
                final_cost = round(final_cost, 2)
                exemption = round(exemption, 2)

                lines.append({
                    'cost_name': cost.name,
                    'product': product.name,
                    'hs_code': hs_code,
                    'country': country.name if country else '',
                    'cost_price': round(cost_price, 2),
                    'original_cost': original_cost,
                    'final_cost': final_cost,
                    'exemption': exemption,
                })

        return {
            'docs': docs,
            'lines': lines,
        }