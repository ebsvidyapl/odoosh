from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    hs_code = fields.Char(string="HS Code")

    country_of_origin_id = fields.Many2one(
        'res.country',
        string="Country of Origin"
    )