from odoo import models, api

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    @api.model
    def create(self, vals_list):
        records = super().create(vals_list)

        # Loop for multi-create safety
        for record in records:

            # Apply only if Sales Officer creates leave
            if self.env.user.has_group('employee_management.group_sales_officer'):

                management_group = self.env.ref(
                    'employee_management.group_management',
                    raise_if_not_found=False
                )

                if management_group:
                    # Get all management users
                    users = self.env['res.users'].search([
                        ('groups_id', 'in', management_group.id),
                        ('share', '=', False)
                    ])

                    for user in users:
                        self.env['mail.activity'].create({
                            'res_model_id': self.env['ir.model']._get_id('hr.leave'),
                            'res_id': record.id,
                            'user_id': user.id,
                            'summary': 'Time Off Request',
                            'note': f'{self.env.user.name} requested time off.',
                            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                        })

        return records