# -*- coding: utf-8 -*-
{
    'name': "e-Way Bill System",

    'summary': "E-way Bill System",

    'description': "",

    'author': "Sai Application",
    'website': "http://www.saiaipl.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Tax Payment',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
       
        'wizard/create_eway_bill_view.xml',
        'wizard/ewaybill_download.xml'
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    'installable': True,
    'auto_install': False,
    'application': True,
    
}