from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    approval_state2 = fields.Selection([
        ('draft', 'Pending Approval'),
        ('approved', 'Approved')
    ], default='draft')