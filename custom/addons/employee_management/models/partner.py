from odoo import models, fields, api
from odoo.exceptions import AccessError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    approval_state = fields.Selection([
        ('draft', 'Pending Approval'),
        ('approved', 'Approved')
    ], default='draft', string="Approval Status")
    @api.model
    def create(self, vals):
        user = self.env.user

        if user.has_group('employee_management.group_sales_officer') or \
           user.has_group('employee_management.group_logistics'):
            vals['approval_state'] = 'draft'
        else:
            vals['approval_state'] = 'approved'

        return super().create(vals)
    def write(self, vals):
         if 'approval_state' not in vals:
            for rec in self:
                if rec.approval_state != 'approved' and not self.env.user.has_group('employee_management.group_management'):
                    raise AccessError("You cannot modify unapproved customers/vendors.")
                return super().write(vals)
    def action_approve(self):
        if not self.env.user.has_group('employee_management.group_management'):
            raise AccessError("Only Management can approve.")
        self.write({'approval_state': 'approved'})  
    