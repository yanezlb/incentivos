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


def limpiar_texto(texto):
    return "".join(caracter for caracter in texto if caracter.isalpha())

def get_badge_estatus(estatus):
    estatus = limpiar_texto(estatus)
    return f'<span class="badge badge-{"success" if estatus == "REGISTRADO" else "danger"}">{estatus}</span>'