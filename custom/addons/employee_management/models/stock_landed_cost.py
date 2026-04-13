from odoo import models


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    def compute_landed_cost(self):
        """
        Apply exemption BEFORE computation (CORRECT WAY)
        """

        for cost in self:
            for cost_line in cost.cost_lines:

                product = cost_line.product_id
                if not product:
                    continue

                # ✅ CLEAN HS CODE
                hs_code = (product.product_tmpl_id.hs_code or '')
                hs_code = hs_code.replace('.', '').replace(' ', '').strip()

                country = product.country_of_origin_id

                # ✅ FIND RULE
                rules = self.env['customs.exemption.rule'].search([
                    ('active', '=', True)
                ])

                matched_rule = False

                for rule in rules:
                    rule_hs = (rule.hs_code or '')
                    rule_hs = rule_hs.replace('.', '').replace(' ', '').strip()

                    if (
                        rule_hs == hs_code
                        and rule.country_id.id == country.id
                    ):
                        matched_rule = rule
                        break

                # ✅ APPLY ON COST LINE (NOT adjustment line)
                if matched_rule:

                    if matched_rule.exemption_type == 'full':
                        cost_line.price_unit = 0.0

                    elif matched_rule.exemption_type == 'partial':
                        reduction = cost_line.price_unit * (
                            matched_rule.exemption_percentage / 100.0
                        )
                        cost_line.price_unit -= reduction

        # ✅ NOW let Odoo compute correctly
        return super().compute_landed_cost()