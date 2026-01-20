# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('PEDIDOS'), False, URL('admin', 'default', 'site')),
    (T('MIS DATOS'), False, URL('admin', 'default', 'site')),
    (T('REPORTES'), False, '#', [
        (T('ENTREGAS'), False, URL('admin', 'default', 'design/')),
        (T('TRABAJADORES'), False,
            URL(
                'admin', 'default', 'edit//controllers/.py')),
        (T('UBICACIÓN'), False,
            URL(
                'admin', 'default', 'edit//views/')),
        (T('OPERATIVO'), False,
            URL(
                'admin', 'default', 'edit//models/db.py')),
        ]),
    (T('ADMINISTRACIÓN'), False, '#', [
        (T('TRABAJADORES'), False, URL('admin', 'default', 'site')),
        (T('ALMACENES'), False, URL('admin', 'default', 'site')),
        (T('OPERATIVOS'), False, URL('admin', 'default', 'site')),
    ]),
    (T('CONTACTO'), False, URL('admin', 'default', 'site')),
]

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if not configuration.get('app.production'):
    _app = request.application
    response.menu += [
        
    ]

