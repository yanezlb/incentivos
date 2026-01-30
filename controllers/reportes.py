# -*- coding: utf-8 -*-

def entregas():
    grid = SQLFORM.grid(db.pedido_operativo)
    
    return dict(grid=grid)