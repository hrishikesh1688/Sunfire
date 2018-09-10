{
    'name': 'my_pucrhase_inhe',
    'version': '11.0.1.0.0',
    'category': 'my_category',
    'author': 'SAI AIPL',
    'depends': ['purchase','sale','sunfire_sales'],
    'data': [
        'security/security_groups.xml',
        'views/purchase_view.xml',
        'wizard/create_purchase_order_view.xml',
        'views/sale_invoice_list.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
