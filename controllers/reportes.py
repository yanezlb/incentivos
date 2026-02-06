# -*- coding: utf-8 -*-
    

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

    por_estado = db((db.pedido_operativo.id_usuario == db.auth_user.id) & (db.pedido_operativo.estatus == 'REGISTRADO')).select(
        db.auth_user.id_estado, contador, 
        groupby=db.auth_user.id_estado
    )


    return dict(
        total_pedidos=total_pedidos,
        por_operativo=por_operativo,
        entes=por_ente,
        negocios=por_negocio,
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
        grid=grid
    )


@auth.requires_login()
def trabajadores():
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

    por_estado = db((db.pedido_operativo.id_usuario == db.auth_user.id)).select(
        db.pedido_operativo.id_operativo, db.auth_user.id_estado, db.pedido_operativo.estatus, contador,
        groupby=(db.pedido_operativo.id_operativo, db.auth_user.id_estado, db.pedido_operativo.estatus)
    )


    return dict(
        total=total,
        entes=por_ente,
        negocios=por_negocio,
        estados=por_estado,
        grid=grid
    )