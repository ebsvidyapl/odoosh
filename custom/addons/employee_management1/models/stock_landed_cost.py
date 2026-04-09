from odoo import models

class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    def _get_customs_exemption(self, product):
        rule = self.env['customs.exemption.rule'].search([
            ('hs_code', '=', product.hs_code),
            ('country_id', '=', product.country_of_origin_id.id),
            ('active', '=', True)
        ], limit=1)

        return rule

    def button_validate(self):
        res = super().button_validate()

        for cost in self:
            for line in cost.valuation_adjustment_lines:
                product = line.product_id
                rule = self._get_customs_exemption(product)

                if rule:
                    if rule.exemption_type == 'full':
                        line.additional_landed_cost = 0
                    elif rule.exemption_type == 'partial':
                        reduction = (
                            line.additional_landed_cost *
                            rule.exemption_percentage / 100
                        )
                        line.additional_landed_cost -= reduction

        return res