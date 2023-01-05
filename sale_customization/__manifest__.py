# -*- coding: utf-8 -*-
{
    'name': 'Sale Customization',
    'version': '1.08',
    'category': 'sale',
    'description': u"""

""",
    'author': 'Empact',
    'depends': [
        'base',
        'sale',
        'sale_management',
        'account'

    ],
    'data': [
        # 'security/product_security.xml',
        # 'security/ir.model.access.csv',
        'data/automation.xml',
        'report/custom_sale_report.xml',
        'report/external_layout_boxed_cust.xml',
        'report/invoice_report.xml',
        'report/delivery_report.xml',
        'views/delivery_template.xml',
        'views/invoice_template.xml',
        'views/sale_order_template.xml',

    ],
    'application': True,
}