{
    'name': 'Employee Management',
    'version': '19.0.1',
    'summary': 'Simple Employee Management Module',
    'author': 'Vidhya',
    'category': 'Human Resources',
    'license': 'LGPL-3',
    'depends': ['base','sale', 'hr', 'purchase'],
    'data': [
        'security/security.xml',        
        'security/ir.model.access.csv', 
        'security/record_rules.xml',

        'data/employee_sequence.xml',

        'reports/employee_report.xml',
        'reports/employee_report_template.xml',
        
        'views/res_partner_views.xml',
        'views/employee_views.xml',
        'views/sale_order_views.xml',      
        'views/purchase_order_views.xml',

    ],
    'installable': True,
    'application': True,
}