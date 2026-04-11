from odoo import models, fields, api


class CustomsExemptionRule(models.Model):
    _name = 'customs.exemption.rule'
    _description = 'Customs Exemption Rule'

    name = fields.Char(required=True)

    hs_code = fields.Char(required=True)
    country_id = fields.Many2one('res.country', required=True)

    exemption_type = fields.Selection([
        ('full', 'Full Exemption'),
        ('partial', 'Partial Exemption')
    ], default='full')

    exemption_percentage = fields.Float(string="Exemption %")

    active = fields.Boolean(default=True)

    # ✅ AUTO UPPERCASE FIX
    @api.model
    def create(self, vals):
        if vals.get('hs_code'):
            vals['hs_code'] = vals['hs_code'].upper().strip()
        return super().create(vals)

    def write(self, vals):
        if vals.get('hs_code'):
            vals['hs_code'] = vals['hs_code'].upper().strip()
        return super().write(vals)