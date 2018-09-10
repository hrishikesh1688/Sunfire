{
    'name': 'Sunfire Timesheet',
    'version': '11.0.1.0.0',
    'category': 'timesheet',
    'author': 'Jeevan',
    'maintainer': 'SAIAIPL',
    #'Images':['static/src/img/icon.png',]
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'views/sunfire_timesheet_views.xml',
        'views/timesheet_master_views.xml',
    ],
    'depends':['sunfire_sales'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
