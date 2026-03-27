from odoo import models, fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    lead_time = fields.Integer(string='Lead Time (Days)')