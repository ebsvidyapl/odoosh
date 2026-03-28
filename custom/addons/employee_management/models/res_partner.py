from odoo import models, fields, api
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    approval_state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved')
    ], default='draft')

    def action_submit(self):
        self.approval_state = 'pending'

    def action_approve(self):
        if not self.env.user.has_group('employee_management.group_management'):
            raise UserError("Only Management can approve")
        self.approval_state = 'approved'
    @api.model
    def create(self, vals):
        user = self.env.user
        if user.has_group('employee_management.group_sales_team'):
         vals['approval_state'] = 'pending'
        else:
            vals['approval_state'] = 'approved'
        return super().create(vals)

    def write(self, vals):
        user = self.env.user
        if user.has_group('employee_management.group_sales_team'):
          raise UserError("You cannot edit without approval!")
        return super().write(vals)