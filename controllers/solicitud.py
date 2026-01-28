# -*- coding: utf-8 -*-

from datetime import datetime

@auth.requires_login()
def pedidos():
    """
    Controlador para la gestión de pedidos en la solicitud.
    Permite listar, agregar, editar y eliminar pedidos.
    """

    # Obtener la fecha actual (solo fecha, sin hora)
    hoy = datetime.today().date()

    # Consulta a la tabla operativo con join a operativo_combo, filtrando
    # por intervalo [fecha_inicio_solicitud, fecha_fin_solicitud] que incluya hoy
    operativos_vigentes = db(
        (db.operativo.fecha_inicio_solicitud <= hoy) &
        (db.operativo.fecha_fin_solicitud >= hoy) &
        (db.operativo.id == db.operativo_combo.id_operativo)
    ).select(db.operativo.ALL, db.operativo_combo.ALL).first()

    links = [
        dict(
            header='Acciones',  # Título de la columna
            body=lambda row: A(
                'Entregar',
                _class='btn btn-primary',
                _type='submit',
                _href=URL('solicitud', 'confirmar_pedido_entregado', args=[row.id])
            ) if row.estatus[0] != 'ENTREGADO' else ''
        )
    ]
    
    # Lógica para manejar las operaciones CRUD de pedidos
    campos = [field for field in db.pedido_operativo if field.name != 'id']
    qry = (db.pedido_operativo.id_usuario == auth.user_id)
    grid = SQLFORM.grid(qry, csv=False, 
                        fields=campos, 
                        links=links, 
                        details=False,
                        editable=False,  
                        deletable=False,
                        create=False,
                        searchable=False)

    # Devolvemos también los operativos vigentes por si se necesitan en la vista
    return dict(grid=grid, operativos_vigentes=operativos_vigentes)


def get_estatus(lista):
    return lista[0]
    

def confirmar_pedido_entregado():
    """
    Controlador para la confirmación de pedidos en la solicitud.
    Permite confirmar un pedido específico.
    """
    pedido_id = request.args(0)
    pedido = db.pedido_operativo(pedido_id)

    if pedido:
        # Lógica para confirmar el pedido
        pedido.update_record(estatus='ENTREGADO')

    redirect(URL('solicitud', 'pedidos'))


def confirmar_pedido_entregado_registrado():
    """
    Controlador para registrar un pedido operativo con estatus REGISTRADO.
    """
    id_operativo = request.vars.id_operativo
    id_operativo_combo = request.vars.id_operativo_combo
    id_usuario = request.vars.id_usuario

    # Validar que no exista ya un registro con la misma combinación
    existe = db(
        (db.pedido_operativo.id_operativo == id_operativo) &
        (db.pedido_operativo.id_operativo_combo == id_operativo_combo) &
        (db.pedido_operativo.id_usuario == id_usuario)
    ).count()

    if not existe:
        # Insertar el pedido operativo con estatus REGISTRADO
        db.pedido_operativo.insert(
            id_operativo=id_operativo,
            id_operativo_combo=id_operativo_combo,
            id_usuario=id_usuario,
            estatus='REGISTRADO'
        )

    redirect(URL('solicitud', 'pedidos'))


@auth.requires_login()
def entregas():
    """
    Controlador para la gestión de entregas en la solicitud.
    Permite listar, agregar, editar y eliminar entregas.
    """

    # Obtener la fecha actual (solo fecha, sin hora)
    hoy = datetime.today().date()

    # Consulta a la tabla operativo con join a operativo_combo, filtrando
    # por intervalo [fecha_inicio_solicitud, fecha_fin_solicitud] que incluya hoy
    operativos_vigentes = db(
        (db.operativo.fecha_inicio_solicitud <= hoy) &
        (db.operativo.fecha_fin_solicitud >= hoy) &
        (db.operativo.id == db.operativo_combo.id_operativo)
    ).select(db.operativo.ALL, db.operativo_combo.ALL).first()

    links = [
        dict(
            header='Acciones',  # Título de la columna
            body=lambda row: A(
                'Entregar',
                _class='btn btn-primary',
                _type='submit',
                _href=URL('solicitud', 'confirmar_pedido_entregado', args=[row.id])
            ) if row.estatus[0] != 'ENTREGADO' else ''
        )
    ]
    
    # Lógica para manejar las operaciones CRUD de pedidos
    campos = [field for field in db.pedido_operativo if field.name != 'id']
    qry = (db.pedido_operativo.id_usuario == auth.user_id)
    grid = SQLFORM.grid(qry, csv=False, 
                        fields=campos, 
                        links=links, 
                        details=False,
                        editable=False,  
                        deletable=False,
                        create=False,
                        searchable=False)

    # Devolvemos también los operativos vigentes por si se necesitan en la vista
    return dict(grid=grid, operativos_vigentes=operativos_vigentes)