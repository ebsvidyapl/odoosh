from odoo import models


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    def _create_valuation_adjustment_lines(self):
     

        res = super()._create_valuation_adjustment_lines()

        for cost in self:
            for line in cost.valuation_adjustment_lines:

                product = line.product_id

                if not product:
                    continue

                # Normalize HS Code
                hs_code = (product.product_tmpl_id.hs_code or '').replace('.', '').strip()
                country_id = product.country_of_origin_id.id

                # Find rule
                rule = self.env['customs.exemption.rule'].search([
                    ('hs_code', '=', hs_code),
                    ('country_id', '=', country_id),
                    ('active', '=', True)
                ], limit=1)

                # Apply exemption
                if rule:
                    if rule.exemption_type == 'full':
                        line.additional_landed_cost = 0.0

                    elif rule.exemption_type == 'partial':
                        reduction = line.additional_landed_cost * (rule.exemption_percentage / 100.0)
                        line.additional_landed_cost -= reduction

        return res