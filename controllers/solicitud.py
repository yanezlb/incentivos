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
    operativo_vigente = db(
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
                        details=False,
                        editable=False,  
                        deletable=False,
                        create=False,
                        searchable=False)

    # Devolvemos también los operativos vigentes por si se necesitan en la vista
    return dict(grid=grid, operativo_vigente=operativo_vigente)


def get_estatus(lista):
    return lista[0]


def confirmar_pedido_entregado():
    """
    Controlador para la confirmación de pedidos en la solicitud.
    Permite confirmar un pedido específico.
    """
    pedido_id = request.args(0)
    pedido = db.pedido_operativo(pedido_id)
    db.pedido_operativo.id.readable = False 

    if pedido:
        # Lógica para confirmar el pedido
        pedido.update_record(estatus='ENTREGADO')

    id_registro = request.args(0)
    record = db.pedido_operativo(id_registro) or redirect(URL('index'))
    
    # Solo mostramos el campo observaciones
    form = SQLFORM(db.pedido_operativo, record, fields=['observaciones'], buttons=[TAG.button('Guardar', _type="submit", _class="btn btn-primary")])

    if form.process().accepted:
        # Respuesta especial para cerrar el modal y refrescar la tabla
        return SCRIPT("jQuery('#observaciones_frm').modal('hide'); window.location.reload();")
        
    return form
    


def confirmar_pedido_registrado():
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

    # 1. Formulario para capturar la cédula
    form = SQLFORM.factory(
        Field('cedula', 'string', label='Cédula', requires=IS_NOT_EMPTY())
    )

    filtro = None
    if form.process(formname='form_cedula').accepted:
        filtro = form.vars.cedula

    links = [
        dict(
            header='Acciones',  # Título de la columna
            body=lambda row: 
                A(
                    'Entregar',
                    _class='btn btn-info btn-xs',
                    _onclick=f"abrirModal('{row.pedido_operativo.id}')",
                    _style="cursor:pointer"
                ) if row.pedido_operativo.estatus[0] != 'ENTREGADO' else ''
        )
    ]
    
    # 2. Consulta con join a auth_user usando id_usuario
    campos = [field for field in db.pedido_operativo if field.name != 'id']
    campos += [db.auth_user.cedula]
    # join lógico: pedido_operativo.id_usuario == auth_user.id
    qry = (db.pedido_operativo.id_usuario == db.auth_user.id)
    if filtro:
        # Si tienes campo cedula en auth_user, filtra por ahí
        qry &= (db.auth_user.cedula == filtro)

    grid = SQLFORM.grid(qry,
                        csv=False,
                        fields=campos,
                        links=links,
                        details=False,
                        editable=False,
                        deletable=False,
                        create=False,
                        searchable=False)

    return dict(grid=grid, form=form)