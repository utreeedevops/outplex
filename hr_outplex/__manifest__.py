# -*- coding: utf-8 -*-
{
    'name': "Nómina Outplex",
    'summary': """Este Modulo agrega customizaciones de la nomina de Outplex a Odoo""",
    'description': """Nómina Outplex""",
    'author': "Pablo Yoel Mercedes Poché, Utreee",
    'category': 'Human Resources',
    'version': '1.0.1',
    'license': '',
    'depends': [
        'hr',
        'hr_contract',
        'hr_payroll'
    ],
    'support': 'https://www.utreee.com/?page_id=3509&lang=es',
    'data': [
        # 'security/ir.model.access.csv',
        'views/hr_attendance_view.xml',
        'views/hr_contract_view.xml',
        'views/hr_payslip_view.xml',
        # 'data/salary_rule_categories.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}