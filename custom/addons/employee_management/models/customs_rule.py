from odoo import models, fields

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

    exemption_percentage = fields.Float(
        string="Exemption %",
        help="Used if partial exemption"
    )

    active = fields.Boolean(default=True)