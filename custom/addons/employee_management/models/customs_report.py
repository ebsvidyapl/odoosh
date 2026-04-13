from odoo import models


class CustomsReport(models.AbstractModel):
    _name = 'report.employee_management.report_customs'
    _description = 'Customs Exemption Report'

    def _get_report_values(self, docids, data=None):

        docs = self.env['stock.landed.cost'].browse(docids)

        lines = []

        for cost in docs:

            data_lines = cost.valuation_adjustment_lines or cost.cost_lines

            for line in data_lines:

                product = False

                if hasattr(line, 'product_id') and line.product_id:
                    product = line.product_id
                elif hasattr(line, 'move_id') and line.move_id:
                    product = line.move_id.product_id

                if not product:
                    continue

                tmpl = product.product_tmpl_id

                lines.append({
                    'cost_name': cost.name,
                    'product': product.name,
                    'hs_code': tmpl.hs_code or '',
                    'country': tmpl.country_of_origin_id.name if tmpl.country_of_origin_id else '',
                    'original_duty': getattr(line, 'original_duty', 0.0),
                    'applied_duty': getattr(line, 'applied_duty', 0.0),
                    'exemption': getattr(line, 'exemption_amount', 0.0),
                    'type': getattr(line, 'exemption_type', 'none'),
                })

        return {
            'docs': docs,
            'lines': lines,
        }