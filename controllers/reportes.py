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
    form = SQLFORM.factory(
        Field('id_region', db.region, label='Región', requires=IS_IN_DB(db, 'region.id', '%(nombre)s', zero='Seleccione una región')),
        Field('id_operativo', db.operativo, label='Operativo', requires=IS_IN_DB(db, 'operativo.id', '%(nombre)s', zero='Seleccione un operativo')),
        submit_button='Buscar',
        keepvalues=True
    )

    filtros = (db.pedido_operativo.id_almacen == db.almacen.id) & (db.pedido_operativo.estatus == 'ENTREGADO')

    if form.process().accepted:
        # aplicar filtros según formulario
        # print("Form accepted with values:", form.vars.id_region, form.vars.id_operativo)
        if form.vars.id_region:
            filtros &= (db.almacen.id_region == form.vars.id_region)
        if form.vars.id_operativo:
            filtros &= (db.pedido_operativo.id_operativo == form.vars.id_operativo)
    elif form.errors:
        errores_txt = '; '.join(
        f"{campo}: {msg}" for campo, msg in form.errors.items()
    )
        response.flash = errores_txt

    
    fields = [
        db.almacen.id_region,
        db.pedido_operativo.id_operativo,
        db.pedido_operativo.id_almacen,
        db.almacen.nombre,
        db.pedido_operativo.id_usuario,
        db.pedido_operativo.id_usuario_entrega,
        db.pedido_operativo.id_usuario_retiro,
        db.pedido_operativo.estatus
    ]

    grid = SQLFORM.grid(db(filtros), 
                        fields=fields,
                        csv=False, 
                        create=False, 
                        editable=False, 
                        deletable=False,
                        searchable=False,
                        user_signature=False,
                        maxtextlength=50)

    # 1. Total global de pedidos (con los mismos filtros)
    total_pedidos = db((db.pedido_operativo.id_usuario == db.auth_user.id) & filtros).count()

    # Definimos el contador para las agrupaciones
    contador = db.auth_user.id.count()

    por_operativo = db((db.pedido_operativo.id_usuario == db.auth_user.id) & filtros).select(
        db.pedido_operativo.id_operativo, contador, 
        groupby=db.pedido_operativo.id_operativo
    )

    por_ente = db((db.pedido_operativo.id_usuario == db.auth_user.id) & filtros).select(
        db.auth_user.id_ente, contador, 
        groupby=db.auth_user.id_ente
    )

    por_negocio = db((db.pedido_operativo.id_usuario == db.auth_user.id) & filtros).select(
        db.auth_user.id_negocio, contador, 
        groupby=db.auth_user.id_negocio
    )

    por_region_acopio = db((db.pedido_operativo.id_usuario == db.auth_user.id) & filtros).select(
        db.auth_user.id_region_acopio, contador, 
        groupby=db.auth_user.id_region_acopio
    )


    por_estado = db((db.pedido_operativo.id_usuario == db.auth_user.id) & filtros).select(
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
        grid=grid,
        form=form
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

    return dict(form_operativo=form_operativo)


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
            estado, coalesce(sum(cant_pedidos), 0) cant_pedidos, sum(recepcion) recepcion, sum(entrega_trabajador) entrega_trabajador, sum(despacho_comedor) despacho_comedor, 
            sum(merma) merma, sum(hurto) hurto, sum(recepcion_transferencia) recepcion_transferencia, sum(salida_transferencia) salida_transferencia, sum(casos_especiales) casos_especiales, sum(total_general) total_general
            from pedidos a
            right join movimientos b on a.id_operativo = b.id_operativo
            {filtro}
            group by 1"""
    
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
        region, coalesce(sum(cant_pedidos), 0) cant_pedidos, sum(recepcion) recepcion, sum(entrega_trabajador) entrega_trabajador, sum(despacho_comedor) despacho_comedor, 
        sum(merma) merma, sum(hurto) hurto, sum(recepcion_transferencia) recepcion_transferencia, sum(salida_transferencia) salida_transferencia, sum(casos_especiales) casos_especiales, sum(total_general) total_general  
        from pedidos a
        right join movimientos b on a.id_operativo = b.id_operativo
        {filtro}
        group by 1"""
    
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
        almacen, coalesce(sum(cant_pedidos), 0) cant_pedidos, sum(recepcion) recepcion, sum(entrega_trabajador) entrega_trabajador, sum(despacho_comedor) despacho_comedor, 
        sum(merma) merma, sum(hurto) hurto, sum(recepcion_transferencia) recepcion_transferencia, sum(salida_transferencia) salida_transferencia, sum(casos_especiales) casos_especiales, sum(total_general) total_general  
        from pedidos a
        right join movimientos b on a.id_operativo = b.id_operativo
        {filtro}
        group by 1"""
    
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
        almacen, coalesce(sum(cant_pedidos), 0) cant_pedidos, sum(recepcion) recepcion, sum(entrega_trabajador) entrega_trabajador, sum(despacho_comedor) despacho_comedor, 
        sum(merma) merma, sum(hurto) hurto, sum(recepcion_transferencia) recepcion_transferencia, sum(salida_transferencia) salida_transferencia, sum(casos_especiales) casos_especiales, sum(total_general) total_general  
        from pedidos a
        right join movimientos b on a.id_operativo = b.id_operativo
        {filtro}
        group by 1"""
    
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
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_inventario.xlsx'
    
    return output.read()


def exportar_reporte_entregas():
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Reporte entregas') 
    filtro = ''

    if request.vars.operativo != 'None' and request.vars.operativo is not None:
        filtro = f" where b.id_operativo = {request.vars.operativo}"

    query_almacen = f"""SELECT 
                    b.cedula, b.first_name ||' '|| b.last_name nombre, b.fecha_nacimiento, 
                    c.nombre ente, d.nombre negocio, e.nombre region_acopio, 'S' recibo_combo, e.nombre region, 
                    a.entrega_tiempo, f.first_name ||' '|| f.last_name nombre_operador, a.observaciones
                    FROM public.pedido_operativo a
                    join auth_user b on a.id_usuario = b.id
                    join ente c on b.id_ente = c.id
                    join negocio d on b.id_negocio = d.id
                    join region e on b.id_region_acopio = e.id
                    join auth_user f on a.id_usuario_entrega = b.id
                    where a.estatus like '%ENTREGADO%'
                    ORDER BY 1 ASC """
    
    datos_almacen = db.executesql(query_almacen, as_ordered_dict=True)

    header_format = workbook.add_format({
        'bold': True,
        'font_name': 'Arial',
        'font_size': 13,
        'font_color': '#FFFFFF',
        'bg_color': '#E60000',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'
    })

    data_format = workbook.add_format({
        'font_name': 'Arial',
        'border': 1
    })

    columnas = [
         'CÉDULA', 'NOMBRE', 'FECHA NACIMIENTO', 'ENTE', 
         'NEGOCIO', 'REGIÓN ACOPIO', 'RECIBO COMBO', 'REGIÓN', 
         'TIEMPO ENTREGA', 'NOMBRE ENTREGA', 'OBSERVACIONES']

    for col_num, titulo in enumerate(columnas):
        worksheet.write(3, col_num, titulo, header_format)
        worksheet.set_column(col_num, col_num, 20)

    for row_num, fila in enumerate(datos_almacen, start=4):
        worksheet.write(row_num, 0, fila['cedula'], data_format)
        worksheet.write(row_num, 1, fila['nombre'], data_format)
        worksheet.write(row_num, 2, fila['fecha_nacimiento'], data_format)
        worksheet.write(row_num, 3, fila['ente'], data_format)
        worksheet.write(row_num, 4, fila['negocio'], data_format)
        worksheet.write(row_num, 5, fila['region_acopio'], data_format)
        worksheet.write(row_num, 6, fila['recibo_combo'], data_format)
        worksheet.write(row_num, 7, fila['region'], data_format)
        worksheet.write(row_num, 8, fila['entrega_tiempo'], data_format)
        worksheet.write(row_num, 9, fila['nombre_operador'], data_format)
        worksheet.write(row_num, 10, fila['observaciones'], data_format)

    workbook.close()
    output.seek(0)
    
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_entregas.xlsx'
    
    return output.read()