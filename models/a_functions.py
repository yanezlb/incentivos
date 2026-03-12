# -*- coding: utf-8 -*-
from datetime import datetime

TIPO_MOV_RECEPCION = 'Recepción'
TIPO_MOV_ENTREGA = 'Entrega Trabajador'
TIPO_MOV_COMEDOR = 'Despacho a Comedor'
TIPO_MOV_MERMA = 'Merma'
TIPO_MOV_HURTO = 'Hurto'
TIPO_MOV_CASOS_ESP = 'Casos Especiales'
TIPO_MOV_SALIDA_TRANS = 'Salida por Transferencia'
TIPO_MOV_RECEPCION_TRANS = 'Recepción por Transferencia'

EST_MOV_BORRADOR = 'Borrador'
EST_MOV_VALIDADO = 'Validado'
EST_MOV_CONFIRMAR = 'Por confirmar'
EST_MOV_ANULADO = 'Anulado'


def formato_fecha(fecha_original):
    return fecha_original.strftime("%d/%m/%Y")


def transformar_fecha(fecha_str):
    fecha_str = fecha_str.strftime('%Y-%m-%d')
    return fecha_str


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
    return f'<span class="badge badge-{"danger" if estatus == "REGISTRADO" else "success"}">{estatus}</span>'


def get_badge_estatus_operativo(estatus):
    estatus = db.estatus_operativo(estatus).nombre
    return f'<span class="badge badge-{"danger" if estatus == "REGISTRADO" else "success"}">{estatus}</span>'


def get_badge_estatus_movimiento(estatus):
    
    if isinstance(estatus, int):
        estatus = db.estatus_movimiento(estatus).nombre

    return f'<span class="badge badge-{"danger" if estatus == EST_MOV_BORRADOR or estatus == EST_MOV_CONFIRMAR else "info"}">{estatus}</span>'


def get_badge_tipo_movimiento(id_tipo_movimiento):
    tipo_movimiento = ''
    signo = None
    if isinstance(id_tipo_movimiento, int):
        signo = db.tipo_movimiento(id_tipo_movimiento).signo
        tipo_movimiento = db.tipo_movimiento(id_tipo_movimiento).nombre

    return f'<span class="badge badge-{"danger" if signo < 0 else "success"}">{tipo_movimiento}</span>'


def insertar_movimiento(id_operativo, id_almacen, tipo_movimiento_txt=TIPO_MOV_ENTREGA, estatus_movimiento_txt=EST_MOV_VALIDADO, cantidad=1, observaciones=None, id_almacen_transferencia=None):
    try:
        if isinstance(tipo_movimiento_txt, str):
            id_tipo_movimiento = db(db.tipo_movimiento.nombre == tipo_movimiento_txt).select().first().id
        else:
            id_tipo_movimiento = tipo_movimiento_txt

        id_estatus_movimiento = db(db.estatus_movimiento.nombre == estatus_movimiento_txt).select().first().id

        db.tipo_movimiento(nombre='Entrada')
        nuevo_id = db.movimiento.insert(
            id_operativo=id_operativo,
            id_almacen=id_almacen,
            id_tipo_movimiento=id_tipo_movimiento,
            id_estatus_movimiento=id_estatus_movimiento,
            id_almacen_transferencia=id_almacen_transferencia,
            cantidad=cantidad,
            observaciones=observaciones
        )

        return nuevo_id
    
    except Exception as e:
        print(f"Error al insertar movimiento: {e}")
        return None