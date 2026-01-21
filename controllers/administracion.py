# -*- coding: utf-8 -*-

def almacen():
    """
    Controlador para la gestión de almacenes en la administración.
    Permite listar, agregar, editar y eliminar almacenes.
    """
    # Lógica para manejar las operaciones CRUD de almacenes
    grid = SQLFORM.grid(db.almacen)

    return dict(grid=grid)