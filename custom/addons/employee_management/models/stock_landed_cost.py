from odoo import models, fields


class StockValuationAdjustmentLines(models.Model):
    _inherit = 'stock.valuation.adjustment.lines'

    purchase_cost = fields.Float(string="Purchase Cost")
    duty_fee = fields.Float(string="Duty Fee")
    exemption_applied = fields.Float(string="Exemption Applied")


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

                # ✅ PURCHASE COST
                line.purchase_cost = product.standard_price or 0.0

                # ✅ APPLY ONLY TO DUTY LINES
                cost_line_name = (line.cost_line_id.name or '').lower()

                if 'duty' not in cost_line_name:
                    line.duty_fee = 0.0
                    line.exemption_applied = 0.0
                    continue

                base_duty = line.additional_landed_cost or 0.0

                # FIND RULE
                rule = self.env['customs.exemption.rule'].search([
                    ('hs_code', '=', hs_code),
                    ('country_id', '=', country.id if country else False),
                    ('active', '=', True)
                ], limit=1)

                # ==========================
                # FULL EXEMPTION (DUTY FREE)
                # ==========================
                if rule and rule.exemption_type == 'full':

                    line.duty_fee = 0.0
                    line.exemption_applied = 0.0
                    line.additional_landed_cost = 0.0

                # ==========================
                # PARTIAL EXEMPTION
                # ==========================
                elif rule and rule.exemption_type == 'partial':

                    reduction = base_duty * (rule.exemption_percentage / 100.0)
                    final_duty = base_duty - reduction

                    line.duty_fee = final_duty
                    line.exemption_applied = reduction
                    line.additional_landed_cost = final_duty

                # ==========================
                # NO EXEMPTION
                # ==========================
                else:
                    line.duty_fee = base_duty
                    line.exemption_applied = 0.0

        return res