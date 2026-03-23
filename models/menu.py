# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------
if auth.user:
        # El usuario está logueado
    response.menu = [
        (T('INICIO'), False, URL('default', 'index')),
        (T('PEDIDOS'), False, URL('solicitud', 'pedidos')),
        (T('MIS DATOS'), False, URL('administracion', 'mis_datos')),
        (T('CONTACTO'), False, URL('default', 'contacto')),
    ]

    if auth.has_membership(ROL_ADMINISTRADOR_CORPORATIVO):
        response.menu = [
            (T('INICIO'), False, URL('default', 'index')),
            (T('PEDIDOS'), False, URL('solicitud', 'pedidos')),
            (T('ENTREGAS'), False, URL('solicitud', 'entregas')),
            (T('MIS DATOS'), False, URL('administracion', 'mis_datos')),
            (T('REPORTES'), False, '#', [
                (T('PEDIDOS'), False, URL('reportes', 'pedidos')),
                (T('ENTREGAS'), False, URL('reportes', 'entregas')),
                (T('TRABAJADORES'), False, URL('reportes', 'trabajadores')),
                (T('UBICACIÓN'), False, URL('reportes', 'ubicacion')),
                (T('OPERATIVO'), False, URL('reportes', 'operativos')),
                (T('INVENTARIO'), False, URL('reportes', 'inventario')),
            ]),
            (T('ADMINISTRACIÓN'), False, '#', [
                (T('TRABAJADORES'), False, URL('administracion', 'trabajadores')),
                (T('DESACTIVAR TRABAJADORES'), False, URL('administracion', 'desactivar_usuarios')),
                (T('ALMACENES'), False, URL('administracion', 'almacen')),
                (T('OPERATIVOS'), False, URL('administracion', 'operativo')),
                (T('INVENTARIO'), False, URL('administracion', 'inventario')),
                (T('USUARIOS'), False, URL('administracion', 'usuarios')),
            ]),
            (T('CONTACTO'), False, URL('default', 'contacto')),
        ] 

    if auth.has_membership(ROL_ADMINISTRADOR_REGIONAL):
        response.menu = [
            (T('INICIO'), False, URL('default', 'index')),
            (T('PEDIDOS'), False, URL('solicitud', 'pedidos')),
            (T('ENTREGAS'), False, URL('solicitud', 'entregas')),
            (T('MIS DATOS'), False, URL('administracion', 'mis_datos')),
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

