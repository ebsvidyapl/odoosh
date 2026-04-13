from odoo import models


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    def button_validate(self):
        """
        Apply exemption ONLY on freight before validation
        """

        for cost in self:
            for line in cost.valuation_adjustment_lines:

                product = line.product_id
                if not product:
                    continue

                # ✅ CLEAN HS CODE
                hs_code = (product.product_tmpl_id.hs_code or '')
                hs_code = hs_code.replace('.', '').replace(' ', '').strip()

                # ✅ COUNTRY
                country = product.country_of_origin_id

                # 🔍 DEBUG (REMOVE AFTER TEST)
                print("------ DEBUG START ------")
                print("PRODUCT:", product.name)
                print("HS CODE:", hs_code)
                print("COUNTRY:", country.name if country else "None")

                # ✅ GET ALL ACTIVE RULES
                rules = self.env['customs.exemption.rule'].search([
                    ('active', '=', True)
                ])

                matched_rule = False

                # ✅ MATCH MANUALLY (ROBUST)
                for rule in rules:
                    rule_hs = (rule.hs_code or '')
                    rule_hs = rule_hs.replace('.', '').replace(' ', '').strip()

                    if (
                        rule_hs == hs_code
                        and rule.country_id.id == country.id
                    ):
                        matched_rule = rule
                        break

                print("MATCHED RULE:", matched_rule)

                # ✅ APPLY EXEMPTION ONLY ON FREIGHT
                if matched_rule:

                    if matched_rule.exemption_type == 'full':
                        print("FULL EXEMPTION APPLIED")
                        line.additional_landed_cost = 0.0

                    elif matched_rule.exemption_type == 'partial':
                        reduction = line.additional_landed_cost * (
                            matched_rule.exemption_percentage / 100.0
                        )
                        print("PARTIAL EXEMPTION:", reduction)
                        line.additional_landed_cost -= reduction

                else:
                    print("NO RULE MATCHED")

                print("------ DEBUG END ------")

        return super().button_validate()