{
    'name': 'Sunfire Sales Tweak',
    'version': '11.0.1.0.0',
    'summary': 'Sunfire Sales Tweak',
    'category': 'Sales',
    'author': 'Jeevan',
    'maintainer': 'Jeevan',
    'website': 'www.saiaipl.com',
    'license': 'AGPL-3',
    'depends': [
        'sale','product','sale_margin','account','purchase','crm',
    ],
    'data': [
        'security/security_group.xml',
        'views/sunfire_sale_views.xml',
        'views/res_partner_views.xml',
        'views/sunfire_master_menu_views.xml',
        #'views/sunfire_purchase_views.xml',
        'views/trees_view.xml',
        'wizard/sunfire_import_view.xml',
        # 'report/sales_quat_report.xml',
        # 'report/sales_order.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
