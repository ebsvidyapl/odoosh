from odoo import models


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    def _get_valuation_lines(self):
        """
        Override to apply customs exemption BEFORE landed cost computation
        """

        lines = super()._get_valuation_lines()

        for line in lines:
            product_id = line.get('product_id')
            if not product_id:
                continue

            # Get product
            product = self.env['product.product'].browse(product_id)

            # Get HS Code from TEMPLATE (important!)
            hs_code = (product.product_tmpl_id.hs_code or '').replace('.', '').strip()

            # Get country
            country_id = product.country_of_origin_id.id

            # Search matching exemption rule
            rule = self.env['customs.exemption.rule'].search([
                ('hs_code', '=', hs_code),
                ('country_id', '=', country_id),
                ('active', '=', True)
            ], limit=1)

            # Apply exemption if rule found
            if rule:
                additional_cost = line.get('additional_landed_cost', 0.0)

                if rule.exemption_type == 'full':
                    line['additional_landed_cost'] = 0.0

                elif rule.exemption_type == 'partial':
                    reduction = additional_cost * (rule.exemption_percentage / 100.0)
                    line['additional_landed_cost'] = additional_cost - reduction

        return lines