from odoo import models


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    def _get_customs_exemption(self, product):

     product_hs = (product.product_tmpl_id.hs_code or '').replace('.', '').strip()

     rule = self.env['customs.exemption.rule'].search([
        ('hs_code', '=', product_hs),
        ('country_id', '=', product.country_of_origin_id.id),
        ('active', '=', True)
    ], limit=1)

     return rule

    def _get_valuation_lines(self):
        lines = super()._get_valuation_lines()

        for line in lines:
            product = line.get('product_id')
            if not product:
                continue

            product_obj = self.env['product.product'].browse(product)
            rule = self._get_customs_exemption(product_obj)

            if rule:
                additional_cost = line.get('additional_landed_cost', 0)

                if rule.exemption_type == 'full':
                    line['additional_landed_cost'] = 0

                elif rule.exemption_type == 'partial':
                    reduction = additional_cost * rule.exemption_percentage / 100
                    line['additional_landed_cost'] = additional_cost - reduction

        return linest