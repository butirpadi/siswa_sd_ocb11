# -*- coding: utf-8 -*-
{
    'name': "Siswa SD",

    'summary': """
        Integrate siswa module for SD Level """,

    'description': """
        Integrate siswa module for SD Level
    """,

    'author': "Tepat Guna Karya",
    'website': "http://www.tepatguna.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/flectra/flectra/blob/master/flectra/addons/base/module/module_data.xml
    # for the full list
    'category': 'Education',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'siswa_ocb11', 'siswa_keu_ocb11', 'siswa_tab_ocb11', 'siswa_psb_ocb11'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_model_data.xml',
        'views/wizard_naik_kelas.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
} 