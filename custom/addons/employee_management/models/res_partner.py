from odoo import models, fields, api
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    approval_state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved')
    ], default='draft', string="Approval Status")

    approved_by = fields.Many2one('res.users', string="Approved By")

    def action_submit_for_approval(self):
        for rec in self:
            rec.approval_state = 'pending'

    def action_approve_partner(self):
        for rec in self:
            if not self.env.user.has_group('employee_management.group_management'):
                raise UserError("Only Management can approve.")

            rec.approval_state = 'approved'
            rec.approved_by = self.env.user.id
    def write(self, vals):
        for rec in self:
            if (
            rec.approval_state == 'pending'
            and self.env.user.has_group('employee_management.group_sales_team')
        ):
                raise UserError("Waiting for management approval.")
        return super().write(vals)