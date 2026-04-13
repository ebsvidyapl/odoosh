from odoo import models

class CustomsReport(models.AbstractModel):
    _name = 'report.employee_management.report_customs'
    _description = 'Customs Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.landed.cost'].browse(docids)

        eur = self.env.ref('base.EUR')
        aed = self.env.company.currency_id

        lines = []

        for doc in docs:
            for val in doc.valuation_adjustment_lines:

                product = val.product_id
                if not product:
                    continue

                # ✅ 1. GET PURCHASE PRICE (REAL EUR VALUE)
                purchase_line = False

                if val.move_id:
                    purchase_line = val.move_id.purchase_line_id

                if purchase_line:
                    cost_price_eur = purchase_line.price_unit or 0.0
                    purchase_currency = purchase_line.order_id.currency_id
                else:
                    cost_price_eur = 0.0
                    purchase_currency = eur

                # ❗ DO NOT reconvert if already EUR
                if purchase_currency != eur:
                    cost_price_eur = purchase_currency._convert(
                        cost_price_eur,
                        eur,
                        doc.company_id,
                        doc.date
                    )

                # ✅ Convert purchase → AED
                cost_price_aed = eur._convert(
                    cost_price_eur,
                    aed,
                    doc.company_id,
                    doc.date
                )

                # ✅ 2. FREIGHT (ALWAYS AED IN ODOO)
                freight_aed = val.additional_landed_cost or 0.0

                # Convert AED → EUR
                freight_eur = aed._convert(
                    freight_aed,
                    eur,
                    doc.company_id,
                    doc.date
                )

                # ✅ 3. EXEMPTION (ONLY ON FREIGHT)
                exemption_aed = 0.0

                hs_code = (product.product_tmpl_id.hs_code or '').replace('.', '').strip()
                country_id = product.country_of_origin_id.id

                rule = self.env['customs.exemption.rule'].search([
                    ('hs_code', '=', hs_code),
                    ('country_id', '=', country_id),
                    ('active', '=', True)
                ], limit=1)

                if rule:
                    if rule.exemption_type == 'full':
                        exemption_aed = freight_aed
                    elif rule.exemption_type == 'partial':
                        exemption_aed = freight_aed * (rule.exemption_percentage / 100.0)

                # Convert exemption → EUR
                exemption_eur = aed._convert(
                    exemption_aed,
                    eur,
                    doc.company_id,
                    doc.date
                )

                # ✅ 4. TOTALS
                total_eur = cost_price_eur + freight_eur - exemption_eur
                total_aed = cost_price_aed + freight_aed - exemption_aed

                lines.append({
                    'product': product.name,
                    'hs_code': product.product_tmpl_id.hs_code or '',
                    'country': product.country_of_origin_id.name or '',

                    'cost_price_eur': cost_price_eur,
                    'cost_price_aed': cost_price_aed,

                    'freight_eur': freight_eur,
                    'freight_aed': freight_aed,

                    'exemption_eur': exemption_eur,
                    'exemption_aed': exemption_aed,

                    'total_eur': total_eur,
                    'total_aed': total_aed,
                })

        return {
            'docs': docs,
            'lines': lines,
        }