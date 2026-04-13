from odoo import models, fields


# ✅ EXTEND VALUATION LINE
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


# ✅ MAIN LOGIC
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

                # ❗ APPLY ONLY TO DUTY LINES
                cost_line_name = (line.cost_line_id.name or '').lower()
                if 'duty' not in cost_line_name:
                    # Non-duty → no exemption logic
                    line.original_duty = line.additional_landed_cost or 0.0
                    line.applied_duty = line.additional_landed_cost or 0.0
                    line.exemption_amount = 0.0
                    line.exemption_type = 'none'
                    continue

                # FIND RULE
                rule = self.env['customs.exemption.rule'].search([
                    ('hs_code', '=', hs_code),
                    ('country_id', '=', country.id if country else False),
                    ('active', '=', True)
                ], limit=1)

                base_amount = line.additional_landed_cost or 0.0

                # ==========================
                # ✅ FULL EXEMPTION (DUTY FREE)
                # ==========================
                if rule and rule.exemption_type == 'full':

                    # ❗ DUTY NEVER EXISTS
                    line.original_duty = 0.0
                    line.additional_landed_cost = 0.0
                    line.applied_duty = 0.0
                    line.exemption_amount = 0.0
                    line.exemption_type = 'full'

                # ==========================
                # ✅ PARTIAL EXEMPTION
                # ==========================
                elif rule and rule.exemption_type == 'partial':

                    line.original_duty = base_amount

                    reduction = base_amount * (rule.exemption_percentage / 100.0)
                    final = base_amount - reduction

                    line.additional_landed_cost = final
                    line.applied_duty = final
                    line.exemption_amount = reduction
                    line.exemption_type = 'partial'

                # ==========================
                # ✅ NO RULE
                # ==========================
                else:
                    line.original_duty = base_amount
                    line.applied_duty = base_amount
                    line.exemption_amount = 0.0
                    line.exemption_type = 'none'

        return res