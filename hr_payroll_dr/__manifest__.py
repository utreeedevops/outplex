# -*- coding: utf-8 -*-
{
    'name': "Nómina Dominicana Utree",
    'summary': """Adaptación de la nómina en odoo para República Dominicana""",
    'description': """Nómina Dominicana""",
    'author': "Pablo Yoel Mercedes Poché, Utree",
    'category': 'Human Resources',
    'version': '1.0.0',
    'license': '',
    'depends': [
        'hr',
        'hr_contract',
        'hr_payroll'
    ],
    'support': 'https://www.utreee.com/?page_id=3509&lang=es',
    'data': [
        'security/ir.model.access.csv',
        'wizards/ministry_labor_wizard_view.xml',
        'views/hr_employee_view.xml',
        'data/salary_rule_categories.xml',
        'data/res_partner.xml',
        # 'data/contribution_register_data.xml',
        'data/hr_payroll_structure_type_data.xml',
        'data/hr_payroll_structure.xml',
        'data/hr_salary_rules.xml',
    ],
    # 'images': ['static/src/img/main_screenshot.png'],
    # 'qweb': ["static/src/xml/org_chart_employee.xml", ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
