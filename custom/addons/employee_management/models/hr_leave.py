from odoo import models, api

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    @api.model
    def create(self, vals):
        record = super(HrLeave, self).create(vals)

        # Check if created by Sales Officer
        sales_group = self.env.ref('employee_management.group_sales_officer')
        management_group = self.env.ref('employee_management.group_management')

        if self.env.user in sales_group.users:
            # Create activity for all management users
            for user in management_group.users:
                self.env['mail.activity'].create({
                    'res_model_id': self.env['ir.model']._get_id('hr.leave'),
                    'res_id': record.id,
                    'user_id': user.id,
                    'summary': 'Time Off Request Approval',
                    'note': f'Sales Officer {self.env.user.name} requested time off.',
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                })

        return record