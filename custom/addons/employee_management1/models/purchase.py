from odoo import models, fields

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    country_of_origin_id = fields.Many2one(
        'res.country',
        string="Country of Origin"
    )