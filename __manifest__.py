# -*- coding: utf-8 -*-
{
    'name': "Seguimiento de recolecta",  # Module title
    'summary': "Módulo para administrar la recolecta entrante",  # Module subtitle phrase
    'description': """
Manage recolecta
==============
Description related to recolecta.
    """,  # Supports reStructuredText(RST) format
    'Deliver': "Parth Gajjar",
    'website': "http://www.example.com",
    'category': 'Tools',
    'version': '14.0.1',
    'depends': ['base'],

    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/recolecta_colecta.xml',
        'views/recolecta_colecta_categ.xml',
        'views/partner.xml',
        'reports/colectas_report.xml',
        # Si no carga demo data, este siempre carga
        #'demo/demo.xml',              
    ],
    # This demo data files will be loaded if db initialize with demo data (commented becaues file is not added in this example)
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,    
}
