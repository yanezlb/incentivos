# -*- coding: utf-8 -*-

from datetime import datetime
from gluon import Field

@auth.requires_login()
def pedidos():
    """
    Controlador para la gestión de pedidos en la solicitud.
    Permite listar, agregar, editar y eliminar pedidos.
    """

    # Obtener la fecha actual (solo fecha, sin hora)
    hoy = datetime.today().date()
    db.pedido_operativo.observaciones.readable = False

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
                        searchable=False,
                        maxtextlength=50)

    # Devolvemos también los operativos vigentes por si se necesitan en la vista
    return dict(grid=grid, operativo_vigente=operativo_vigente)

@auth.requires_login()
def get_estatus(lista):
    return lista[0]


@auth.requires_login()
def confirmar_pedido_entregado():
    pedido_id = request.args(0)
    pedido = db.pedido_operativo(pedido_id)
    id_registro = request.args(0)
    record = db.pedido_operativo(id_registro) or redirect(URL('index'))

    # Si no tiene usuario_retiro, asigna el actual
    cambios = {}
    if not record.id_usuario_entrega:
        cambios['id_usuario_entrega'] = auth.user_id
    if not record.id_usuario_retiro:
        cambios['id_usuario_retiro'] = record.id_usuario
    if cambios:
        record.update_record(**cambios)

    db.pedido_operativo.id.readable = False

    if pedido and pedido.id_operativo:
        db.pedido_operativo.id_almacen.requires = IS_IN_DB(
            db((db.operativo_almacen.id_operativo == pedido.id_operativo) &
               (db.operativo_almacen.id_almacen == db.almacen.id)),
            'almacen.id',
            '%(nombre)s'
        )

    form = SQLFORM(
        db.pedido_operativo,
        record,
        fields=['id_usuario_entrega', 'id_usuario_retiro', 'id_almacen', 'observaciones'],
        buttons=[TAG.button('Guardar', _type="submit", _class="btn btn-primary")]
    )

    if form.process(formname='frm_observaciones').accepted and pedido:
        pedido.update_record(estatus='ENTREGADO', entrega_tiempo=datetime.now())
        result = insertar_movimiento(pedido.id_operativo, form.vars.id_almacen, tipo_movimiento_txt=TIPO_MOV_ENTREGA, estatus_movimiento_txt=EST_MOV_VALIDADO)
        if not result:
            # Si la inserción fue exitosa, podemos hacer algo
            response.flash = "Error al registrar movimiento."

            pass
        return SCRIPT("jQuery('#observaciones_frm').modal('hide'); window.location.reload();")

    return form
    

@auth.requires_login()
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
        Field(
            'cedula',
            'integer',
            label='Cédula',
            requires=[
                IS_NOT_EMPTY(),
                IS_MATCH('^[0-9]{1,12}$', error_message='Solo números, máximo 12 dígitos')
            ],
            length=12
        ),
        submit_button='Buscar'
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
    
    if auth.has_membership(ROL_ADMINISTRADOR_REGIONAL):
        region_id = get_region_por_usuario(auth.user_id)

        if region_id:
            qry &= ((db.pedido_operativo.id_almacen == db.almacen.id) & (db.almacen.id_region_acopio == region_id))

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
                        searchable=False,
                        maxtextlength=50)

    return dict(grid=grid, form=form)