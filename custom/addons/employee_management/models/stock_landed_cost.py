from odoo import models, fields


class StockValuationAdjustmentLines(models.Model):
    _inherit = 'stock.valuation.adjustment.lines'

    original_duty = fields.Float(string="Original Duty")
    applied_duty = fields.Float(string="Applied Duty")
    exemption_amount = fields.Float(string="Exemption Amount")
    exemption_type = fields.Selection([
        ('none', 'No Exemption'),
        ('full', 'Full Exemption'),
        ('partial', 'Partial Exemption')
    ], default='none')


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    def button_validate(self):

        res = super().button_validate()

        for cost in self:
            for line in cost.valuation_adjustment_lines:

                move = line.move_id
                if not move:
                    continue

                product = move.product_id
                tmpl = product.product_tmpl_id

                hs_code = (tmpl.hs_code or '').strip().upper()
                country = tmpl.country_of_origin_id

                if not hs_code or not country:
                    continue

                # Find rule
                rule = self.env['customs.exemption.rule'].search([
                    ('hs_code', '=', hs_code),
                    ('country_id', '=', country.id),
                    ('active', '=', True)
                ], limit=1)

                # Store original duty BEFORE change
                original = line.additional_landed_cost or 0.0
                line.original_duty = original

                if not rule:
                    line.applied_duty = original
                    line.exemption_amount = 0.0
                    line.exemption_type = 'none'
                    continue

                # ✅ FULL EXEMPTION
                if rule.exemption_type == 'full':

                    line.additional_landed_cost = 0.0
                    line.applied_duty = 0.0

                    # IMPORTANT: Business meaning → no exemption value
                    line.exemption_amount = 0.0
                    line.exemption_type = 'full'

                # ✅ PARTIAL EXEMPTION
                elif rule.exemption_type == 'partial':

                    reduction = original * (rule.exemption_percentage / 100.0)
                    final = original - reduction

                    line.additional_landed_cost = final
                    line.applied_duty = final

                    line.exemption_amount = reduction
                    line.exemption_type = 'partial'

        return res