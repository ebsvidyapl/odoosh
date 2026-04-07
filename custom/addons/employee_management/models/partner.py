from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    approval_state = fields.Selection([
        ('draft', 'Pending Approval'),
        ('approved', 'Approved')
    ], default='draft')