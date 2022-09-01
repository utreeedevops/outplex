# -*- coding: utf-8 -*-
{
    'name': "Web Employee Support",
    'summary': """Módulo para la Integración de Soportes y Solicitudes Web a los Empleados""",
    'description': """Web Employee Support""",
    'author': "Pablo Yoel Mercedes Poché, Utree",
    'category': 'Human Resources',
    'version': '1.0',
    'depends': ['base', 'hr', 'web', 'website'],
    'price': 0.00,
    'currency': 'US',
    # 'support': 'frejusarnaud@gmail.com',
    'data': [
        'security/ir.model.access.csv',
        'views/website_employees_general_request_form.xml',
        'views/employee_request_view.xml',
        'data/payslip_web_mail.xml',
    ],
    # 'images': ['static/src/img/main_screenshot.png'],
    # 'qweb': ["static/src/xml/org_chart_employee.xml", ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
