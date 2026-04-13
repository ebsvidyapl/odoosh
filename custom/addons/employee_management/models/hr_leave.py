from odoo import models, api

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    @api.model
    def create(self, vals):
        record = super().create(vals)

        # Check if current user is Sales Officer
        if self.env.user.has_group('employee_management.group_sales_officer'):

            management_group = self.env.ref('employee_management.group_management')

            # Get users safely (Odoo 19 compatible)
            users = self.env['res.users'].search([
                ('groups_id', 'in', management_group.id)
            ])

            for user in users:
                self.env['mail.activity'].create({
                    'res_model_id': self.env['ir.model']._get_id('hr.leave'),
                    'res_id': record.id,
                    'user_id': user.id,
                    'summary': 'Time Off Request Approval',
                    'note': f'Sales Officer {self.env.user.name} requested time off.',
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                })

        return record