# -*- coding: utf-8 -*-

def pedidos():
    """
    Controlador para la gestión de pedidos en la solicitud.
    Permite listar, agregar, editar y eliminar pedidos.
    """

    links = [
        dict(
            header='Acciones', # Título de la columna
            body=lambda row: A('Entregar', 
                               _class='button btn btn-default btn-secondary', 
                               _href=URL('confirmar_pedido', args=[row.id])) if row.estatus[0] != 'ENTREGADO' else ''
        )
    ]
    
    # Lógica para manejar las operaciones CRUD de pedidos
    campos = [field for field in db.pedido_operativo if field.name != 'id']
    qry = (db.pedido_operativo.id_usuario == auth.user_id)
    grid = SQLFORM.grid(qry, csv=False, 
                        fields=campos, 
                        links=links, 
                        details=False,
                        editable=False,  # Deshabilita el botón de "Editar"
                        deletable=False,  # Deshabilita el botón de "Eliminar"
                        create=False)

    return dict(grid=grid)

def get_estatus(lista):
    return lista[0]
    


def confirmar_pedido():
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