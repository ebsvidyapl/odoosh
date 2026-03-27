from odoo import models, fields, api

class Employee(models.Model):
    _name = 'employee.management'
    _description = 'Employee Management'
    employee_code = fields.Char(
        string="Employee ID",
        readonly=True,
        copy=False,
        default="New"
    )
    name = fields.Char(string="Employee Name", required=True,
        help="Enter the full name of the employee.")
    age = fields.Integer(string="Age",
        help="Enter the age.")
    email = fields.Char(string="Email",
        help="Enter the email.")
    department_id = fields.Many2one(
    'hr.department',
    string="Department"
)
    salary = fields.Float(string="Salary")

    phone = fields.Char(string="Phone")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")

    date_of_birth = fields.Date(string="Date of Birth")
    address = fields.Text(string="Address")
    annual_salary = fields.Float(
        string="Annual Salary",
        compute="_compute_annual_salary"
    )

    @api.depends('salary')
    def _compute_annual_salary(self):
        for record in self:
            record.annual_salary = record.salary * 12
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['employee_code'] = self.env['ir.sequence'].next_by_code('employee.management') or 'New'
        return res