# -*- coding: utf-8 -*-

{
    'name': 'Insumar_check_credit',
    'version': '1.1.01',
    'category': 'General',
    'summary': '',
    'description': """
    Revision y aviso de credito de clientes

       """,
    'author' : 'M.Gah',
    'website': '',
    'depends': ['base','sale','account','l10n_cl_fe','parches_insumar'],
    'data': [
        "security/groups.xml",
        "views/res_partner.xml"
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
