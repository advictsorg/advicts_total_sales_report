# -*- coding: utf-8 -*-
{
    'name': "Advicts Salesperson Sales & Payments Report",
    'summary': """ Report to Calculate the Sales and Payments of Sales Person depend on Date (from - to) """,
    'description': """ Report to Calculate the Sales and Payments of Sales Person depend on Date (from - to) """,
    'author': "GhaithAhmed@Advicts",
    'website': "https://advicts.com",
    'category': 'Accounting',
    'version': '1.0',
    'depends': ['base', 'sale', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/report_wizard.xml',
        'views/views.xml',
        'reports/reports.xml',
        'reports/report_template.xml',
    ],
}
