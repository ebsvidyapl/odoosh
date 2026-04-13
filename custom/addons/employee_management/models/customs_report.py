from odoo import models


class CustomsReport(models.AbstractModel):
    _name = 'report.employee_management.report_customs'
    _description = 'Customs Report'

    def _get_report_values(self, docids, data=None):

        docs = self.env['stock.landed.cost'].browse(docids)

        lines = []

        for cost in docs:
            for line in cost.valuation_adjustment_lines:

                product = line.product_id or line.move_id.product_id

                if not product:
                    continue

                tmpl = product.product_tmpl_id

                lines.append({
                    'cost_name': cost.name,
                    'product': product.name,
                    'hs_code': tmpl.hs_code or '',
                    'country': tmpl.country_of_origin_id.name if tmpl.country_of_origin_id else '',
                    'purchase_cost': line.purchase_cost,
                    'duty_fee': line.duty_fee,
                    'exemption': line.exemption_applied,
                })

        return {
            'docs': docs,
            'lines': lines,
        }