{
    'name': 'Employee Management',
    'version': '19.0.2',
    'summary': 'Simple Employee Management Module',
    'author': 'Vidhya',
    'category': 'Human Resources',
    'license': 'LGPL-3',
    'depends': ['base','sale', 'hr', 'purchase' , 'crm','sale_management', 'stock'],
    'data': [
        'security/security.xml',        
        'security/ir.model.access.csv',

        'data/employee_sequence.xml',

        'reports/employee_report.xml',
        'reports/employee_report_template.xml',
        
        
        'views/employee_views.xml',
        'views/sale_order_views.xml',      
        'views/purchase_order_views.xml',
         'views/product_views.xml',
        'views/customs_rule_views.xml',
        'views/landed_cost_views.xml',
        'views/report_views.xml',
       # 'views/menu.xml',

    ],
    'installable': True,
    'application': True,
}