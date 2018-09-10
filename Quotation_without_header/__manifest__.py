{
    'name': "Quotation without Report",
    'summary': "Quotation Report Custome",
    'description': """*************************************""",

    'author': "Sai Application",
    'website': "http://www.saiaipl.com",
    'category': 'Uncategorized',
    'version': '11.0.1.0.0',
    # any module necessary for this one to work correctly
    'depends': ['web','sale',],
    # always loaded
    'data': [
        'report/menu_with.xml',
        # 'security/ir.model.access.csv',
        'report/sale_report_templates_without_amount.xml',
        'report/sales_quat_report_without_header.xml',
        
        
    ],
    # only loaded in demonstration mode
}