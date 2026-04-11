from odoo import models


class CustomsReport(models.AbstractModel):
    _name = 'report.customs_management.report_customs'
    _description = 'Customs Report'

    def _get_report_values(self, docids, data=None):

        docs = self.env['stock.landed.cost'].browse(docids)

        report_lines = []

        for cost in docs:
            for line in cost.valuation_adjustment_lines:

                move = line.move_id
                if not move:
                    continue

                product = move.product_id
                tmpl = product.product_tmpl_id

                hs_code = tmpl.hs_code
                country = tmpl.country_of_origin_id.name

                original_cost = line.former_cost
                new_cost = line.additional_landed_cost

                exemption_amount = original_cost - new_cost

                report_lines.append({
                    'cost_name': cost.name,
                    'product': product.name,
                    'hs_code': hs_code,
                    'country': country,
                    'original_cost': original_cost,
                    'new_cost': new_cost,
                    'exemption': exemption_amount,
                })

        return {
            'docs': docs,
            'lines': report_lines,
        }