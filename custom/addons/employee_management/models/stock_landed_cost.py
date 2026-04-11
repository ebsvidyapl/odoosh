from odoo import models
import logging

_logger = logging.getLogger(__name__)


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    def _compute_landed_cost(self):
        """
        Apply customs exemption AFTER Odoo computes landed cost
        """

        # Step 1: let Odoo compute normally
        res = super()._compute_landed_cost()

        # Step 2: apply your logic
        for cost in self:
            for line in cost.valuation_adjustment_lines:

                product = line.product_id

                if not product:
                    continue

                # ✅ CORRECT SOURCE
                tmpl = product.product_tmpl_id

                hs_code = (tmpl.hs_code or '').strip().upper()
                country = tmpl.country_of_origin_id

                if not hs_code or not country:
                    continue

                # ✅ DEBUG LOG
                _logger.info(f"Checking HS: {hs_code}, Country: {country.name}")

                rule = self.env['customs.exemption.rule'].search([
                    ('hs_code', '=', hs_code),
                    ('country_id', '=', country.id),
                    ('active', '=', True)
                ], limit=1)

                if not rule:
                    _logger.info("No rule found")
                    continue

                _logger.info(f"Rule found: {rule.name}")

                # ✅ APPLY EXEMPTION
                if rule.exemption_type == 'full':
                    line.additional_landed_cost = 0.0

                elif rule.exemption_type == 'partial':
                    line.additional_landed_cost *= (
                        1 - (rule.exemption_percentage / 100.0)
                    )

        return res