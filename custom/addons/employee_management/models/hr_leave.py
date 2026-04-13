from odoo import models, api

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    @api.model
    def create(self, vals):
        # Only apply for Sales Officer
        if self.env.user.has_group('employee_management.group_sales_officer'):

            # Get Management group
            management_group = self.env.ref(
                'employee_management.group_management',
                raise_if_not_found=False
            )

            if management_group:
                # Get one management user (Jaikumar)
                management_user = self.env['res.users'].search([
                    ('groups_id', 'in', management_group.id),
                    ('share', '=', False)
                ], limit=1)

                if management_user:
                    # 🔥 FORCE assign approver (THIS FIXES ADMIN ISSUE)
                    vals['holiday_manager_id'] = management_user.id

        # Create record
        record = super().create(vals)

        # 🔔 Create activity for management user
        if record.holiday_manager_id:
            self.env['mail.activity'].create({
                'res_model_id': self.env['ir.model']._get_id('hr.leave'),
                'res_id': record.id,
                'user_id': record.holiday_manager_id.id,
                'summary': 'Time Off Request',
                'note': f'{self.env.user.name} requested time off.',
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            })

        return record