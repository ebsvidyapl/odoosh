from odoo import models


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    def _compute_landed_cost(self):
        """
        Apply customs exemption based on HS Code + Country
        """

        # Step 1: Run original Odoo logic
        res = super()._compute_landed_cost()

        # Step 2: Apply exemption on valuation lines (CORRECT PLACE)
        for cost in self:
            for line in cost.valuation_adjustment_lines:

                product = line.product_id  # ✅ actual inventory product

                if not product:
                    continue

                # Get HS Code from product template
                hs_code = (product.product_tmpl_id.hs_code or '').replace('.', '').strip()

                # Get Country
                country_id = product.country_of_origin_id.id

                # Find matching rule
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

        # Step 3: Recompute totals (IMPORTANT)
        for cost in self:
            total = sum(cost.valuation_adjustment_lines.mapped('additional_landed_cost'))
            cost.amount_total = total

        return res