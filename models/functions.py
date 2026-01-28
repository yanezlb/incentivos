# -*- coding: utf-8 -*-

def formato_fecha(fecha_original):
    return fecha_original.strftime("%d/%m/%Y")


def get_estatus_operativo(id_estatus):
    estatus = db.estatus_operativo(id_estatus)
    return estatus.nombre if estatus else "Desconocido"


def valida_operativo_pedido(id_operativo, id_operativo_combo, id_usuario):
    pedido = db((db.pedido_operativo.id_operativo == id_operativo) &
                (db.pedido_operativo.id_usuario == id_usuario) &
                (db.pedido_operativo.id_operativo_combo == id_operativo_combo)
               ).count()
    return pedido == 0