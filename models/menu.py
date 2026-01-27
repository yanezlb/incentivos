# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------
if auth.user:
        # El usuario está logueado
    response.menu = [
        (T('PEDIDOS'), False, URL('default', 'index')),
        (T('MIS DATOS'), False, URL('default', 'index')),
        (T('REPORTES'), False, '#', [
            (T('ENTREGAS'), False, URL('default', 'index')),
            (T('TRABAJADORES'), False,
                URL('default', 'index')),
            (T('UBICACIÓN'), False,
                URL('default', 'index')),
            (T('OPERATIVO'), False,
                URL('default', 'index')),
            ]),
        (T('ADMINISTRACIÓN'), False, '#', [
            (T('TRABAJADORES'), False, URL('administracion', 'usuarios')),
            (T('ALMACENES'), False, URL('administracion', 'almacen')),
            (T('OPERATIVOS'), False, URL('administracion', 'operativo')),
        ]),
        (T('CONTACTO'), False, URL('default', 'contacto')),
    ]
else:
    # No hay usuario logueado
    response.menu = []


# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if not configuration.get('app.production'):
    _app = request.application
    response.menu += []

