# -*- coding: utf-8 -*-

{
    'name': 'Insumar_check_credit',
    'version': '1.0.02',
    'category': 'General',
    'summary': '',
    'description': """


       """,
    'author' : 'M.Gah',
    'website': '',
    'depends': ['base','sale','account','l10n_cl_fe'],
    'data': [
        "security/groups.xml",
        "views/res_partner.xml"
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
