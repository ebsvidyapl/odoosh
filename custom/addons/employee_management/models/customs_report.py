from odoo import models


class CustomsReport(models.AbstractModel):
    _name = 'report.customs_management.report_customs'
    _description = 'Customs Exemption Report'

    def _get_report_values(self, docids, data=None):

        docs = self.env['stock.landed.cost'].browse(docids)

        lines = []

        for cost in docs:
            for line in cost.valuation_adjustment_lines:

                product = line.product_id or line.move_id.product_id
                tmpl = product.product_tmpl_id

                lines.append({
                    'cost_name': cost.name,
                    'product': product.name,
                    'hs_code': tmpl.hs_code or '',
                    'country': tmpl.country_of_origin_id.name or '',
                    'original_duty': round(line.original_duty, 2),
                    'applied_duty': round(line.applied_duty, 2),
                    'exemption': round(line.exemption_amount, 2),
                    'type': line.exemption_type,
                })

        return {
            'docs': docs,
            'lines': lines,
        }