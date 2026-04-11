from odoo import models


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    def _get_landed_cost_lines(self):
        lines = super()._get_landed_cost_lines()

        for cost in self:
            for cost_line in cost.cost_lines:
                product = cost_line.product_id

                if not product:
                    continue

                hs_code = (product.product_tmpl_id.hs_code or '').replace('.', '').strip()
                country_id = product.country_of_origin_id.id

                rule = self.env['customs.exemption.rule'].search([
                    ('hs_code', '=', hs_code),
                    ('country_id', '=', country_id),
                    ('active', '=', True)
                ], limit=1)

                if rule:
                    if rule.exemption_type == 'full':
                        cost_line.price_unit = 0.0

                    elif rule.exemption_type == 'partial':
                        reduction = cost_line.price_unit * (rule.exemption_percentage / 100.0)
                        cost_line.price_unit -= reduction

        return lines