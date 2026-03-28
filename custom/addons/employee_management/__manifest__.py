{
    'name': 'Employee Management',
    'version': '1.0.1',
    'summary': 'Simple Employee Management Module',
    'author': 'Vidhya',
    'category': 'Human Resources',
    'license': 'LGPL-3',
    'depends': ['base','sale', 'hr', 'purchase'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_partner_views.xml', 
        'data/employee_sequence.xml',
        'reports/employee_report.xml',
        'reports/employee_report_template.xml',
        'views/employee_views.xml',
        'views/sale_order_views.xml',      
        'views/purchase_order_views.xml',

    ],
    'installable': True,
    'application': True,
}