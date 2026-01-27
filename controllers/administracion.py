# -*- coding: utf-8 -*-

@auth.requires_login()
def almacen():
    """
    Controlador para la gestión de almacenes en la administración.
    Permite listar, agregar, editar y eliminar almacenes.
    """
    # Lógica para manejar las operaciones CRUD de almacenes
    campos = [field for field in db.almacen if field.name != 'id']
    grid = SQLFORM.grid(db.almacen, csv=False, fields=campos)

    return dict(grid=grid)



def operativo():
    # Lógica para manejar las operaciones CRUD de operativos
    campos = [
        db.operativo.nombre, 
        db.operativo.fecha_inicio_solicitud,
        db.operativo.fecha_fin_solicitud,
        db.operativo.fecha_inicio_entrega,
        db.operativo.fecha_fin_entrega, 
        db.operativo.id_estatus_operativo]
    
    links = [
        dict(
            header='Acciones', # Título de la columna
            body=lambda row: A('Configurar', 
                               _class='button btn btn-default btn-secondary', 
                               _href=URL('configurar_operativo', args=[row.id]))
        )
    ]

    grid = SQLFORM.grid(db.operativo, csv=False, fields=campos, links=links)

    return dict(grid=grid)


def configurar_operativo():
    # Lógica para manejar las operaciones CRUD de operativos
    registro_id = request.args(0)

    db.operativo_combo.id_operativo.default = registro_id
    db.operativo_combo.id_operativo.writable = False
    db.operativo_combo.id_operativo.readable = False

    query = ((db.operativo_combo.id_operativo == registro_id))
    grid_operativo_combo = SQLFORM.grid(query, csv=False, user_signature=False)
    form_operativo_combo = SQLFORM(db.operativo_combo).process()

    ope_combo_info = db(db.operativo_combo.id_operativo == registro_id).select()

    if form_operativo_combo.accepted:
        response.flash = '¡Datos guardados!'
        redirect(URL('administracion', 'operativo'))
    elif form_operativo_combo.errors:
        response.flash = 'El formulario tiene errores'

    return dict(
            operativo_data=db.operativo(registro_id), 
            grid_operativo_combo=grid_operativo_combo, 
            form_operativo_combo=form_operativo_combo,
            ope_combo_info=ope_combo_info
        )


def usuarios():
    campos = [field for field in db.auth_user if field.name != 'id']

    grid = SQLFORM.grid(db.auth_user, csv=False, fields=campos)

    return dict(grid=grid)