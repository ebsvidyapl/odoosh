from odoo import models
import logging

_logger = logging.getLogger(__name__)


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    def button_compute(self):
        """
        Override compute button to apply customs exemption AFTER Odoo computation
        """

        # Step 1: Let Odoo compute normally
        res = super().button_compute()

        # Step 2: Apply your exemption logic
        for cost in self:
            for line in cost.valuation_adjustment_lines:

                move = line.move_id

                if not move:
                    _logger.info("❌ No move found")
                    continue

                product = move.product_id
                tmpl = product.product_tmpl_id

                hs_code = (tmpl.hs_code or '').strip().upper()
                country = tmpl.country_of_origin_id

                _logger.info(f"Product: {product.name}")
                _logger.info(f"HS: {hs_code}, Country: {country.name}")

                if not hs_code or not country:
                    continue

                rule = self.env['customs.exemption.rule'].search([
                    ('hs_code', '=', hs_code),
                    ('country_id', '=', country.id),
                    ('active', '=', True)
                ], limit=1)

                if not rule:
                    _logger.info("❌ No rule found")
                    continue

                _logger.info(f"✅ Rule applied: {rule.name}")

                # ✅ APPLY EXEMPTION
                if rule.exemption_type == 'full':
                    line.additional_landed_cost = 0.0

                elif rule.exemption_type == 'partial':
                    line.additional_landed_cost *= (
                        1 - (rule.exemption_percentage / 100.0)
                    )

        return res