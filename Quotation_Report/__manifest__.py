{
    'name': "Quotation Report",
    'summary': "Quotation Report Custome",
    'description': """*************************************""",

    'author': "Sai Application",
    'website': "http://www.saiaipl.com",
    'category': 'Uncategorized',
    'version': '11.0.1.0.0',
    # any module necessary for this one to work correctly
    'depends': ['web','sale'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/sales_quat_report.xml',
        'report/sale_report_with_template.xml',
        'report/opf_template.xml',
        'report/OPF.xml',
        'report/menu.xml',
    ],
    # only loaded in demonstration mode
}