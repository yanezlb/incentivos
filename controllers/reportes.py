# -*- coding: utf-8 -*-
import xlsxwriter
from io import BytesIO

@auth.requires_login()
def pedidos():
    grid = SQLFORM.grid(db(db.pedido_operativo.estatus == 'REGISTRADO'), csv=False, create=False, editable=False, deletable=False)

    # 1. Total global de pedidos
    total_pedidos = db((db.pedido_operativo.id_usuario == db.auth_user.id) & (db.pedido_operativo.estatus == 'REGISTRADO')).count()

    # Definimos el contador para las agrupaciones
    contador = db.auth_user.id.count()

    por_operativo = db((db.pedido_operativo.id_usuario == db.auth_user.id) & (db.pedido_operativo.estatus == 'REGISTRADO')).select(
        db.pedido_operativo.id_operativo, contador, 
        groupby=db.pedido_operativo.id_operativo
    )

    por_ente = db((db.pedido_operativo.id_usuario == db.auth_user.id) & (db.pedido_operativo.estatus == 'REGISTRADO')).select(
        db.auth_user.id_ente, contador, 
        groupby=db.auth_user.id_ente
    )

    por_negocio = db((db.pedido_operativo.id_usuario == db.auth_user.id) & (db.pedido_operativo.estatus == 'REGISTRADO')).select(
        db.auth_user.id_negocio, contador, 
        groupby=db.auth_user.id_negocio
    )

    por_region_acopio = db((db.pedido_operativo.id_usuario == db.auth_user.id) & (db.pedido_operativo.estatus == 'REGISTRADO')).select(
        db.auth_user.id_region_acopio, contador, 
        groupby=db.auth_user.id_region_acopio
    )

    por_estado = db((db.pedido_operativo.id_usuario == db.auth_user.id) & (db.pedido_operativo.estatus == 'REGISTRADO')).select(
        db.auth_user.id_estado, contador, 
        groupby=db.auth_user.id_estado
    )


    return dict(
        total_pedidos=total_pedidos,
        por_operativo=por_operativo,
        entes=por_ente,
        negocios=por_negocio,
        regiones=por_region_acopio,
        estados=por_estado,
        grid=grid
    )


@auth.requires_login()
def entregas():
    grid = SQLFORM.grid(db(db.pedido_operativo.estatus == 'ENTREGADO'), csv=False, create=False, editable=False, deletable=False)

    # 1. Total global de pedidos
    total_pedidos = db((db.pedido_operativo.id_usuario == db.auth_user.id) & (db.pedido_operativo.estatus == 'ENTREGADO')).count()

    # Definimos el contador para las agrupaciones
    contador = db.auth_user.id.count()

    por_operativo = db((db.pedido_operativo.id_usuario == db.auth_user.id) & (db.pedido_operativo.estatus == 'ENTREGADO')).select(
        db.pedido_operativo.id_operativo, contador, 
        groupby=db.pedido_operativo.id_operativo
    )

    por_ente = db((db.pedido_operativo.id_usuario == db.auth_user.id) & (db.pedido_operativo.estatus == 'ENTREGADO')).select(
        db.auth_user.id_ente, contador, 
        groupby=db.auth_user.id_ente
    )

    por_negocio = db((db.pedido_operativo.id_usuario == db.auth_user.id) & (db.pedido_operativo.estatus == 'ENTREGADO')).select(
        db.auth_user.id_negocio, contador, 
        groupby=db.auth_user.id_negocio
    )

    por_region_acopio = db((db.pedido_operativo.id_usuario == db.auth_user.id) & (db.pedido_operativo.estatus == 'ENTREGADO')).select(
        db.auth_user.id_region_acopio, contador, 
        groupby=db.auth_user.id_region_acopio
    )


    por_estado = db((db.pedido_operativo.id_usuario == db.auth_user.id) & (db.pedido_operativo.estatus == 'ENTREGADO')).select(
        db.auth_user.id_estado, contador, 
        groupby=db.auth_user.id_estado
    )


    return dict(
        total_pedidos=total_pedidos,
        por_operativo=por_operativo,
        entes=por_ente,
        negocios=por_negocio,
        estados=por_estado,
        regiones=por_region_acopio,
        grid=grid
    )


@auth.requires_login()
def trabajadores():
    ## Para evitar que se muestre el campo email
    db.auth_user.email.writable = False

    grid = SQLFORM.grid(db(db.auth_user), csv=False, deletable=False, create=False)

    return dict(grid=grid)


@auth.requires_login()
def ubicacion():
    grid = SQLFORM.grid(db.auth_user, csv=False, create=False, editable=False, deletable=False)

    # 1. Total global de pedidos
    total_pedidos = db(db.auth_user).count()

    # Definimos el contador para las agrupaciones
    contador = db.auth_user.id.count()

    por_ente = db(db.auth_user).select(
        db.auth_user.id_ente, contador, 
        groupby=db.auth_user.id_ente
    )

    por_negocio = db(db.auth_user).select(
        db.auth_user.id_negocio, contador, 
        groupby=db.auth_user.id_negocio
    )

    por_estado = db(db.auth_user).select(
        db.auth_user.id_estado, contador, 
        groupby=db.auth_user.id_estado
    )


    return dict(
        total_pedidos=total_pedidos,
        entes=por_ente,
        negocios=por_negocio,
        estados=por_estado,
        grid=grid
    )


@auth.requires_login()
def operativos():
    # Cambio de columnas para ocultar los ID en la vista
    db.pedido_operativo.id.readable = False
    db.auth_user.id.readable = False

    grid = SQLFORM.grid(((db.pedido_operativo.id_usuario == db.auth_user.id)), csv=False, create=False, editable=False, deletable=False)

    # 1. Total global de pedidos
    total = db((db.pedido_operativo.id_usuario == db.auth_user.id)).count()

    # Definimos el contador para las agrupaciones
    contador = db.auth_user.id.count()

    por_ente = db((db.pedido_operativo.id_usuario == db.auth_user.id)).select(
        db.pedido_operativo.id_operativo, db.auth_user.id_ente, db.pedido_operativo.estatus, contador,
        groupby=(db.pedido_operativo.id_operativo, db.auth_user.id_ente, db.pedido_operativo.estatus)
    )

    por_negocio = db((db.pedido_operativo.id_usuario == db.auth_user.id)).select(
        db.pedido_operativo.id_operativo, db.auth_user.id_negocio, db.pedido_operativo.estatus, contador,
        groupby=(db.pedido_operativo.id_operativo, db.auth_user.id_negocio, db.pedido_operativo.estatus)
    )

    por_region_acopio = db((db.pedido_operativo.id_usuario == db.auth_user.id)).select(
        db.pedido_operativo.id_operativo, db.auth_user.id_region_acopio, db.pedido_operativo.estatus, contador,
        groupby=(db.pedido_operativo.id_operativo, db.auth_user.id_region_acopio, db.pedido_operativo.estatus)
    )

    por_estado = db((db.pedido_operativo.id_usuario == db.auth_user.id)).select(
        db.pedido_operativo.id_operativo, db.auth_user.id_estado, db.pedido_operativo.estatus, contador,
        groupby=(db.pedido_operativo.id_operativo, db.auth_user.id_estado, db.pedido_operativo.estatus)
    )


    return dict(
        total=total,
        entes=por_ente,
        negocios=por_negocio,
        estados=por_estado,
        regiones=por_region_acopio,
        grid=grid
    )


def inventario():
    filtro = ''

    form_operativo = SQLFORM.factory(
        Field('operativo', db.operativo, label='Operativo', requires=IS_IN_DB(db, 'operativo.id', '%(nombre)s')),
        submit_button='Buscar',
        keepvalues=True
    )

    if form_operativo.process(formname='form_operativo', keepvalues=True).accepted:
        # Usar el valor enviado en el formulario
        filtro = f" where b.id_operativo = {form_operativo.vars.operativo}"
    

    query_almacen = f"""with pedidos as (
            SELECT id_operativo, count(id) cant_pedidos
            FROM public.pedido_operativo
            group by 1
        ),
        movimientos as (
            SELECT 
                d.nombre AS almacen,
                a.id_operativo,
                SUM(CASE WHEN b.nombre = 'Recepción' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS recepcion,
                SUM(CASE WHEN b.nombre = 'Entrega Trabajador' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS entrega_trabajador,
                SUM(CASE WHEN b.nombre = 'Despacho a Comedor' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS despacho_comedor,
                SUM(CASE WHEN b.nombre = 'Merma' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS merma,
                SUM(CASE WHEN b.nombre = 'Hurto' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS hurto,
                SUM(CASE WHEN b.nombre = 'Recepción por Transferencia' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS recepcion_transferencia,
                SUM(CASE WHEN b.nombre = 'Salida por Transferencia' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS salida_transferencia,
                SUM(CASE WHEN b.nombre = 'Casos Especiales' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS casos_especiales,
                SUM(a.cantidad * b.signo * c.factor) AS total_general
            FROM movimiento a
            JOIN tipo_movimiento b ON a.id_tipo_movimiento = b.id
            JOIN estatus_movimiento c ON a.id_estatus_movimiento = c.id
            JOIN almacen d ON a.id_almacen = d.id
            GROUP BY 1, 2
        )
        select 
        almacen, cant_pedidos, recepcion, entrega_trabajador, despacho_comedor, 
        merma, hurto, recepcion_transferencia, salida_transferencia, casos_especiales, total_general  
        right from pedidos a
        join movimientos b on a.id_operativo = b.id_operativo
        {filtro}"""
    
    datos_almacen = db.executesql(query_almacen, as_ordered_dict=True)

    return dict(datos_almacen=datos_almacen, form_operativo=form_operativo)


def inventario_estado():

    filtro = ''
    if request.vars.operativo != 'None' and request.vars.operativo is not None:
        filtro = f" where b.id_operativo = {request.vars.operativo}"

    query_estado = f"""with pedidos as (
            SELECT id_operativo, count(id) cant_pedidos
            FROM public.pedido_operativo
            group by 1
        ),
        movimientos as (
            SELECT 
                e.nombre AS estado,
                a.id_operativo,
                SUM(CASE WHEN b.nombre = 'Recepción' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS recepcion,
                SUM(CASE WHEN b.nombre = 'Entrega Trabajador' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS entrega_trabajador,
                SUM(CASE WHEN b.nombre = 'Despacho a Comedor' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS despacho_comedor,
                SUM(CASE WHEN b.nombre = 'Merma' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS merma,
                SUM(CASE WHEN b.nombre = 'Hurto' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS hurto,
                SUM(CASE WHEN b.nombre = 'Recepción por Transferencia' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS recepcion_transferencia,
                SUM(CASE WHEN b.nombre = 'Salida por Transferencia' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS salida_transferencia,
                SUM(CASE WHEN b.nombre = 'Casos Especiales' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS casos_especiales,
                SUM(a.cantidad * b.signo * c.factor) AS total_general
            FROM movimiento a
            JOIN tipo_movimiento b ON a.id_tipo_movimiento = b.id
            JOIN estatus_movimiento c ON a.id_estatus_movimiento = c.id
            JOIN almacen d ON a.id_almacen = d.id
            JOIN estado e ON d.id_estado = e.id
            GROUP BY 1, 2
        )
        select 
        estado, cant_pedidos, recepcion, entrega_trabajador, despacho_comedor, 
        merma, hurto, recepcion_transferencia, salida_transferencia, casos_especiales, total_general  
        from pedidos a
        right join movimientos b on a.id_operativo = b.id_operativo
        {filtro}"""
    
    datos_estado = db.executesql(query_estado, as_ordered_dict=True)

    return dict(datos_estado=datos_estado)


def inventario_region():

    filtro = ''
    if request.vars.operativo != 'None' and request.vars.operativo is not None:
        filtro = f" where b.id_operativo = {request.vars.operativo}"
    
    query_region = f"""with pedidos as (
            SELECT id_operativo, count(id) cant_pedidos
            FROM public.pedido_operativo
            group by 1
        ),
        movimientos as (
            SELECT 
                e.nombre AS region,
                a.id_operativo,
                SUM(CASE WHEN b.nombre = 'Recepción' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS recepcion,
                SUM(CASE WHEN b.nombre = 'Entrega Trabajador' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS entrega_trabajador,
                SUM(CASE WHEN b.nombre = 'Despacho a Comedor' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS despacho_comedor,
                SUM(CASE WHEN b.nombre = 'Merma' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS merma,
                SUM(CASE WHEN b.nombre = 'Hurto' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS hurto,
                SUM(CASE WHEN b.nombre = 'Recepción por Transferencia' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS recepcion_transferencia,
                SUM(CASE WHEN b.nombre = 'Salida por Transferencia' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS salida_transferencia,
                SUM(CASE WHEN b.nombre = 'Casos Especiales' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS casos_especiales,
                SUM(a.cantidad * b.signo * c.factor) AS total_general
            FROM movimiento a
            JOIN tipo_movimiento b ON a.id_tipo_movimiento = b.id
            JOIN estatus_movimiento c ON a.id_estatus_movimiento = c.id
            JOIN almacen d ON a.id_almacen = d.id
            JOIN region e ON d.id_region = e.id
            GROUP BY 1, 2
        )
        select 
        region, cant_pedidos, recepcion, entrega_trabajador, despacho_comedor, 
        merma, hurto, recepcion_transferencia, salida_transferencia, casos_especiales, total_general  
        from pedidos a
        right join movimientos b on a.id_operativo = b.id_operativo
        {filtro}"""
    
    datos_region = db.executesql(query_region, as_ordered_dict=True)

    return dict(datos_region=datos_region)


def inventario_almacen():

    filtro = ''
    if request.vars.operativo != 'None' and request.vars.operativo is not None:
        filtro = f" where b.id_operativo = {request.vars.operativo}"
    
    query_almacen = f"""with pedidos as (
            SELECT id_operativo, count(id) cant_pedidos
            FROM public.pedido_operativo
            group by 1
        ),
        movimientos as (
            SELECT 
                d.nombre AS almacen,
                a.id_operativo,
                SUM(CASE WHEN b.nombre = 'Recepción' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS recepcion,
                SUM(CASE WHEN b.nombre = 'Entrega Trabajador' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS entrega_trabajador,
                SUM(CASE WHEN b.nombre = 'Despacho a Comedor' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS despacho_comedor,
                SUM(CASE WHEN b.nombre = 'Merma' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS merma,
                SUM(CASE WHEN b.nombre = 'Hurto' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS hurto,
                SUM(CASE WHEN b.nombre = 'Recepción por Transferencia' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS recepcion_transferencia,
                SUM(CASE WHEN b.nombre = 'Salida por Transferencia' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS salida_transferencia,
                SUM(CASE WHEN b.nombre = 'Casos Especiales' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS casos_especiales,
                SUM(a.cantidad * b.signo * c.factor) AS total_general
            FROM movimiento a
            JOIN tipo_movimiento b ON a.id_tipo_movimiento = b.id
            JOIN estatus_movimiento c ON a.id_estatus_movimiento = c.id
            JOIN almacen d ON a.id_almacen = d.id
            GROUP BY 1, 2
        )
        select 
        almacen, cant_pedidos, recepcion, entrega_trabajador, despacho_comedor, 
        merma, hurto, recepcion_transferencia, salida_transferencia, casos_especiales, total_general  
        from pedidos a
        right join movimientos b on a.id_operativo = b.id_operativo
        {filtro}"""
    
    datos_almacen = db.executesql(query_almacen, as_ordered_dict=True)

    return dict(datos_almacen=datos_almacen)

def exportar_reporte():
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Reporte inventario') 
    filtro = ''

    if request.vars.operativo != 'None' and request.vars.operativo is not None:
        filtro = f" where b.id_operativo = {request.vars.operativo}"

    query_almacen = f"""with pedidos as (
            SELECT id_operativo, count(id) cant_pedidos
            FROM public.pedido_operativo
            group by 1
        ),
        movimientos as (
            SELECT 
                d.nombre AS almacen,
                a.id_operativo,
                SUM(CASE WHEN b.nombre = 'Recepción' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS recepcion,
                SUM(CASE WHEN b.nombre = 'Entrega Trabajador' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS entrega_trabajador,
                SUM(CASE WHEN b.nombre = 'Despacho a Comedor' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS despacho_comedor,
                SUM(CASE WHEN b.nombre = 'Merma' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS merma,
                SUM(CASE WHEN b.nombre = 'Hurto' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS hurto,
                SUM(CASE WHEN b.nombre = 'Recepción por Transferencia' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS recepcion_transferencia,
                SUM(CASE WHEN b.nombre = 'Salida por Transferencia' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS salida_transferencia,
                SUM(CASE WHEN b.nombre = 'Casos Especiales' THEN (a.cantidad * b.signo * c.factor) ELSE 0 END) AS casos_especiales,
                SUM(a.cantidad * b.signo * c.factor) AS total_general
            FROM movimiento a
            JOIN tipo_movimiento b ON a.id_tipo_movimiento = b.id
            JOIN estatus_movimiento c ON a.id_estatus_movimiento = c.id
            JOIN almacen d ON a.id_almacen = d.id
            GROUP BY 1, 2
        )
        select 
        almacen, cant_pedidos, recepcion, entrega_trabajador, despacho_comedor, 
        merma, hurto, recepcion_transferencia, salida_transferencia, casos_especiales, total_general  
        from pedidos a
        join movimientos b on a.id_operativo = b.id_operativo
        {filtro}"""
    
    datos_almacen = db.executesql(query_almacen, as_ordered_dict=True)

    header_format = workbook.add_format({
        'bold': True,
        'font_name': 'Arial',
        'font_size': 12,
        'font_color': '#FFFFFF',
        'bg_color': '#2F75B5',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'
    })

    data_format = workbook.add_format({
        'font_name': 'Tahoma',
        'font_color': '#E60000',
        'border': 1
    })

    columnas = ['Almacen', 'Pedidos', 'Recepción', 'Entregas', 'Comedor', 'Merma', 
                'Hurto', 'Transferencia Recep.', 'Salida Trans.', 'Casos especiales', 
                'Disponible']
    for col_num, titulo in enumerate(columnas):
        worksheet.write(0, col_num, titulo, header_format)
        worksheet.set_column(col_num, col_num, 20)

    for row_num, fila in enumerate(datos_almacen, start=1):
        worksheet.write(row_num, 0, fila['almacen'], data_format)
        worksheet.write(row_num, 1, fila['cant_pedidos'], data_format)
        worksheet.write(row_num, 2, fila['recepcion'], data_format)
        worksheet.write(row_num, 3, fila['entrega_trabajador'], data_format)
        worksheet.write(row_num, 4, fila['despacho_comedor'], data_format)
        worksheet.write(row_num, 5, fila['merma'], data_format)
        worksheet.write(row_num, 6, fila['hurto'], data_format)
        worksheet.write(row_num, 7, fila['recepcion_transferencia'], data_format)
        worksheet.write(row_num, 8, fila['salida_transferencia'], data_format)
        worksheet.write(row_num, 9, fila['casos_especiales'], data_format)
        worksheet.write(row_num, 10, fila['total_general'], data_format)

    workbook.close()
    output.seek(0)
    
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_estilizado.xlsx'
    
    return output.read()