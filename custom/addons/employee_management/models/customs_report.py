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

                hs_code = tmpl.hs_code or ''
                country = tmpl.country_of_origin_id.name or ''

                original_cost = line.former_cost or 0.0
                landed_cost = line.additional_landed_cost or 0.0

                exemption = original_cost - landed_cost

                # ✅ Optional: skip zero rows
                # if exemption == 0:
                #     continue

                lines.append({
                    'cost_name': cost.name,
                    'product': product.name,
                    'hs_code': hs_code,
                    'country': country,
                    'original_cost': original_cost,
                    'landed_cost': landed_cost,
                    'exemption': exemption,
                })

        return {
            'docs': docs,
            'lines': lines,
        }