# -*- coding: utf-8 -*-
import os
import pandas as pd


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


@auth.requires_login()
def operativo():
    # Lógica para manejar las operaciones CRUD de operativos
    campos = [
        db.operativo.nombre, 
        db.operativo.fecha_inicio_solicitud,
        db.operativo.fecha_fin_solicitud,
        db.operativo.fecha_inicio_entrega,
        db.operativo.fecha_fin_entrega, 
        db.operativo.id_estatus_operativo
    ]
    count_rows = request.vars.count
    argumentos_formulario = {}

    if request.args(0) == 'edit':
        db.operativo.fecha_inicio_solicitud.writable = False
        db.operativo.fecha_inicio_entrega.writable = False
        db.operativo.fecha_inicio_solicitud.writable = False
        db.operativo.id_estatus_operativo.writable = False
        argumentos_formulario = dict(submit_button='Actualizar')
    
    if request.args(0) == 'new':
        db.operativo.id_estatus_operativo.writable = False
        argumentos_formulario = dict(submit_button='Guardar')
        
    if count_rows:
        response.flash = f"Registros insertados: {count_rows}"
    
    links = [
        dict(
            header='', # Título de la columna
            body=lambda row: A('Configurar', 
                               _class='button btn btn-primary', 
                               _href=URL('configurar_operativo', args=[row.id]))
        ),
        dict(
            header='', # Título de la columna
            body=lambda row: A('Cargar x lotes', 
                               _class='button btn btn-primary', 
                               _href=URL('administracion', 'cargar_lotes', args=[row.id]))
        )
    ]

    grid = SQLFORM.grid(db.operativo, csv=False, fields=campos, links=links, deletable=False, details=False, formargs=argumentos_formulario, maxtextlength=60)

    return dict(grid=grid)


@auth.requires_login()
def cargar_lotes():
    id_operativo = request.args(0)
    id_operativo_combo = request.vars.id_operativo_combo
    datos_operativo = db(db.operativo.id == id_operativo).select().first()

    # 1. Total global de usuarios
    total_usuarios = db(db.auth_user).count()

    # Definimos el contador para las agrupaciones
    contador = db.auth_user.id.count()

    # 2. Total agrupado por Ente
    por_ente = db(db.auth_user).select(
        db.auth_user.id_ente, contador, 
        groupby=db.auth_user.id_ente
    )

    # 3. Total agrupado por Negocio
    por_negocio = db(db.auth_user).select(
        db.auth_user.id_negocio, contador, 
        groupby=db.auth_user.id_negocio
    )

    # 4. Total agrupado por Región
    por_region = db(db.auth_user).select(
        db.auth_user.id_region_acopio, contador, 
        groupby=db.auth_user.id_region_acopio
    )

    # 5. Total agrupado por Estado
    por_estado = db(db.auth_user).select(
        db.auth_user.id_estado, contador, 
        groupby=db.auth_user.id_estado
    )

    form = SQLFORM.factory(
        Field('id_operativo_combo', db.operativo_combo, 
            requires=IS_IN_DB(
                db(db.operativo_combo.id_operativo == id_operativo), 'operativo_combo.id', '%(nombre)s')
            )
    )
    count = 0
    if id_operativo_combo and id_operativo:
        id_operativo = request.args(0)
        id_operativo_combo = request.vars.id_operativo_combo

        usuarios = db(db.auth_user).select()
        
        for usuario in usuarios:
            existe = db((db.pedido_operativo.id_usuario ==  usuario.id) & 
            (db.pedido_operativo.id_operativo == id_operativo) & 
            (db.pedido_operativo.id_operativo_combo == id_operativo_combo)).count()

            if not existe:
                db.pedido_operativo.insert(
                    id_usuario=usuario.id,
                    id_operativo=id_operativo,
                    id_operativo_combo=id_operativo_combo,
                    estatus='REGISTRADO'
                )

                count += 1
            
            db.commit()

        redirect(URL('administracion','operativo', vars={'count': count}))

        response.flash = f"Registros insertados {count}"

    return dict(
        datos_operativo=datos_operativo,
        form=form, total_usuarios=total_usuarios,
        entes=por_ente,
        negocios=por_negocio,
        regiones=por_region,
        estados=por_estado
    )


@auth.requires_login()
def configurar_operativo():
    registro_id = request.args(0)

    db.operativo_combo.id_operativo.default = registro_id
    db.operativo_combo.id_operativo.writable = False
    db.operativo_combo.id_operativo.readable = False

    query = (db.operativo_combo.id_operativo == registro_id)
    grid_operativo_combo = SQLFORM.grid(query, csv=False, user_signature=False)
    form_operativo_combo = SQLFORM(db.operativo_combo).process()

    ope_combo_info = db(db.operativo_combo.id_operativo == registro_id).select()

    if form_operativo_combo.accepted:
        response.flash = '¡Datos guardados!'
        redirect(URL('administracion', 'operativo'))
    elif form_operativo_combo.errors:
        response.flash = 'El formulario tiene errores'

    # ---------- CONFIGURACIÓN DE OPERATIVO_ALMACEN ----------
    db.operativo_almacen.id_operativo.default  = registro_id
    db.operativo_almacen.id_operativo.writable = True
    db.operativo_almacen.id_operativo.readable = True
    db.operativo_almacen.id_almacen.readable = True
    db.operativo_almacen.id_almacen.writable = True

    def validar_operativo_almacen(form):
        id_almacen = form.vars.id_almacen
        if not id_almacen:
            return  # sin almacén no validamos nada

        # En new, form.vars.id suele ser None; en edit, el id del registro
        registro_existente = db(
            (db.operativo_almacen.id_operativo == registro_id) &
            (db.operativo_almacen.id_almacen == id_almacen) &
            (db.operativo_almacen.id != form.vars.id)
        ).count()

        if registro_existente:
            form.errors.id_almacen = 'Ya existe un registro para este operativo y almacén'

    query_almacen = (db.operativo_almacen.id_operativo == registro_id)
    almacenes_grid = SQLFORM.grid(
        query_almacen,
        csv=False,
        user_signature=False,
        searchable=False,
        args=[registro_id],  # mantiene el id en la URL al hacer new/edit
        onvalidation=validar_operativo_almacen
    )

    return dict(
        operativo_data=db.operativo(registro_id),
        grid_operativo_combo=grid_operativo_combo,
        form_operativo_combo=form_operativo_combo,
        ope_combo_info=ope_combo_info,
        almacenes_grid=almacenes_grid
    )


@auth.requires_login()
def usuarios():
    ## Para evitar que se muestre el campo email
    db.auth_user.email.writable = False

    if request.args(0) == 'new':
        db.auth_user.first_name.writable = True
        db.auth_user.last_name.writable = True
        db.auth_user.cedula.writable = True
        db.auth_user.password.writable = True
        db.auth_user.email.writable = True

    campos = [field for field in db.auth_user if field.name != 'id']
    argumentos_formulario = {}
    
    if request.args(0) == 'edit':
        argumentos_formulario = dict(submit_button='Actualizar')
    
    grid = SQLFORM.grid(db.auth_user, csv=False, fields=campos, deletable=False, formargs=argumentos_formulario)

    form = SQLFORM.factory(
        Field('archivo_excel', 'upload', 
              uploadfolder=os.path.join(request.folder, 'uploads'),
              requires=IS_NOT_EMPTY(),
              label="Archivo Excel (.xlsx)")
    )

    if form.process().accepted:
        # Obtenemos el nombre del archivo guardado en la carpeta uploads
        nombre_archivo = form.vars.archivo_excel
        ruta_completa = os.path.join(request.folder, 'uploads', nombre_archivo)
        
        try:
            # Llamamos a la lógica de procesamiento
            resultado = procesar_excel_logica(ruta_completa)
            response.flash = f"Carga exitosa: {resultado} registros procesados."
        except Exception as e:
            response.flash = f"Error en la carga: {str(e)}"
            print({str(e)})
        finally:
            # Opcional: Eliminar el archivo después de procesarlo para no llenar el disco
            # os.unlink(ruta_completa)
            pass
            
    return dict(form=form, grid=grid)


@auth.requires_login()
def desactivar_usuarios():
    campos = [field for field in db.auth_user if field.name != 'id']

    grid = SQLFORM.grid(db.auth_user.is_active==False, csv=False, fields=campos, deletable=False, editable=False)

    form = SQLFORM.factory(
        Field('archivo_excel', 'upload', 
              uploadfolder=os.path.join(request.folder, 'uploads'),
              requires=IS_NOT_EMPTY(),
              label="Archivo Excel (.xlsx)")
    )

    if form.process().accepted:
        # Obtenemos el nombre del archivo guardado en la carpeta uploads
        nombre_archivo = form.vars.archivo_excel
        ruta_completa = os.path.join(request.folder, 'uploads', nombre_archivo)
        
        try:
            # Llamamos a la lógica de procesamiento
            resultado = procesar_desactivar_usuarios(ruta_completa)
            response.flash = f"Carga exitosa: {resultado} registros desactivados."
            # redirect(URL('administracion', 'desactivar_usuarios'))
        except Exception as e:
            response.flash = f"Error en la carga: {str(e)}"
            print({str(e)})
        finally:
            # Opcional: Eliminar el archivo después de procesarlo para no llenar el disco
            # os.unlink(ruta_completa)
            pass
            
    return dict(form=form, grid=grid)

@auth.requires_login()
def procesar_desactivar_usuarios(ruta):
    df = pd.read_excel(ruta)
    conteo = 0
    

    for _, fila in df.iterrows(): 
        trabajador = db((db.auth_user.cedula == fila['Cédula']) & (db.auth_user.is_active == True)).select().first()

        if trabajador: # Validación mínima de que existen las maestras
            db(db.auth_user.cedula == fila['Cédula']).update(
                is_active = False
            )
            conteo += 1
            
    db.commit()
    return conteo


def procesar_excel_logica(ruta):
    df = pd.read_excel(ruta)
    conteo = 0
    for _, fila in df.iterrows():
        # Ejemplo para Región
        reg = db(db.region_acopio.nombre == fila['Region Centro de Acopio']).select().first()
        # Ejemplo para Estado Acopio
        est_acopio = db(db.estado.nombre == fila['Estado Centro Acopio']).select().first()
        # Ejemplo para Estado
        est_administrativo = db(db.estado.nombre == fila['Estado Ubicac Adm']).select().first()
        # Clasificaciones (Ente y Negocio)
        ente = db(db.ente.nombre == fila['CLASIF']).select().first()
        negocio = db(db.negocio.nombre == fila['CLASIF 2']).select().first()
        # 4. Insert en auth_user
        if reg and est_administrativo: # Validación mínima de que existen las maestras
            db.auth_user.update_or_insert(db.auth_user.cedula == fila['Cédula'] ,
                first_name = fila['Nombre y Apellido'].split()[0],
                last_name = fila['Nombre y Apellido'].split()[1],
                email = fila['Correo'],
                cedula = fila['Cédula'],
                id_ente = ente.id if ente else 0,
                id_negocio = negocio.id if negocio else 0,
                id_region_acopio = reg.id,
                id_estado_acopio = est_acopio.id,
                id_estado = est_administrativo.id,
                fecha_nacimiento = transformar_fecha(fila['FNac']),
                fecha_ingreso = transformar_fecha(fila['FECHA DE INGRESO']),
                password = db.auth_user.password.validate('admin')[0] # Pass temporal
            )
            conteo += 1
            
    db.commit()
    return conteo


@auth.requires_login()
def mis_datos():
    usuario_id = auth.user_id
    """
    form = SQLFORM.factory(
            Field('email', requires=[IS_NOT_EMPTY(), IS_EMAIL()], default=db.auth_user(usuario_id).email)
        ).process()

    if form.accepted:
        user = db.auth_user(usuario_id)
        correo = form.vars.email

        user.update_record(email=correo, telefono_oficina=oficina, telefono_celular=celular)

        response.flash = '¡Datos guardados!'
        redirect(URL('administracion', 'mis_datos'))
    elif form.errors:
        response.flash = 'El formulario tiene errores'
    """

    # return dict(form=form, usuario_data=db.auth_user(usuario_id))
    return dict(usuario_data=db.auth_user(usuario_id))


@auth.requires_login()
def inventario():
    campos = [field for field in db.movimiento if field.name != 'id']
    
    if request.args(0) == 'new':
        db.movimiento.id_estatus_movimiento.default = 3 # BORRADOR

    grid = SQLFORM.grid(
        db.movimiento,
        csv=False,
        fields=campos,
        deletable=False,
        editable=lambda row: str(row.id_estatus_movimiento) not in ('4', '6'),
        maxtextlength=60, 
        user_signature=False,
        create=False
    )

    return dict(grid=grid)


@auth.requires_login()
def inventario_transferencia():
    # Formulario para transferencias entre almacenes
    form = SQLFORM.factory(
        Field('operativo', db.operativo, label="Operativo",
              requires=IS_IN_DB(db, 'operativo.id', '%(nombre)s', zero='Seleccione un operativo')),
        Field('id_almacen', db.almacen, label="Almacén origen",
              requires=IS_IN_DB(db, 'almacen.id', '%(nombre)s', zero='Seleccione un almacén')),
        Field('id_almacen_transferencia', db.almacen, label="Almacén de transferencia",
              requires=IS_IN_DB(db, 'almacen.id', '%(nombre)s', zero='Seleccione un almacén de transferencia')),
        Field('cantidad', 'integer', label="Cantidad")
    )

    if form.process().accepted:
        # Aquí iría la lógica de crear el/los movimientos de transferencia
        try:
            result = insertar_movimiento(
                id_operativo=form.vars.operativo,
                id_almacen=form.vars.id_almacen,
                tipo_movimiento_txt=TIPO_MOV_SALIDA_TRANS,
                estatus_movimiento_txt=EST_MOV_VALIDADO,
                id_almacen_transferencia=form.vars.id_almacen_transferencia,
                cantidad=form.vars.cantidad
            )

            result_b =insertar_movimiento(
                id_operativo=form.vars.operativo,
                id_almacen=form.vars.id_almacen,
                tipo_movimiento_txt=TIPO_MOV_RECEPCION_TRANS,
                estatus_movimiento_txt=EST_MOV_VALIDADO,
                id_almacen_transferencia=form.vars.id_almacen_transferencia,
                cantidad=form.vars.cantidad
            )

        except Exception as e:
            response.flash = f"Error al registrar la transferencia: {str(e)}"

        else:
            response.flash = 'Transferencia registrada correctamente.'

    elif form.errors:
        response.flash = f"Error en el formulario: {form.errors}"

    return dict(form=form)


@auth.requires_login()
def inventario_entrada():
    # Formulario para movimientos de entrada
    form = SQLFORM.factory(
        Field('operativo', db.operativo, label="Operativo",
              requires=IS_IN_DB(db, 'operativo.id', '%(nombre)s', zero='Seleccione un operativo')),
        Field('id_tipo_movimiento', db.tipo_movimiento, label="Tipo de Movimiento",
              requires=IS_IN_DB(db(db.tipo_movimiento.signo > 0), 'tipo_movimiento.id', '%(nombre)s', zero='Seleccione un tipo de movimiento')),
        Field('id_almacen', db.almacen, label="Almacén",
              requires=IS_IN_DB(db, 'almacen.id', '%(nombre)s', zero='Seleccione un almacén')),
        Field('cantidad', 'integer', label="Cantidad")
    )

    if form.process().accepted:
        # Aquí iría la lógica de crear el/los movimientos de transferencia
        try:
            result = insertar_movimiento(
                id_operativo=form.vars.operativo,
                id_almacen=form.vars.id_almacen,
                tipo_movimiento_txt=form.vars.id_tipo_movimiento,
                estatus_movimiento_txt=EST_MOV_VALIDADO,
                cantidad=form.vars.cantidad
            )
            
        except Exception as e:
            response.flash = f"Error al registrar la transferencia: {str(e)}"

        else:
            response.flash = 'Movimiento registrada correctamente.'

    elif form.errors:
        response.flash = f"Error en el formulario: {form.errors}"

    return dict(form=form)


@auth.requires_login()
def inventario_salida():
    # Formulario para movimientos de salida
    form = SQLFORM.factory(
        Field('operativo', db.operativo, label="Operativo",
              requires=IS_IN_DB(db, 'operativo.id', '%(nombre)s', zero='Seleccione un operativo')),
        Field('id_tipo_movimiento', db.tipo_movimiento, label="Tipo de Movimiento",
              requires=IS_IN_DB(db(db.tipo_movimiento.signo < 0), 'tipo_movimiento.id', '%(nombre)s', zero='Seleccione un tipo de movimiento')),
        Field('id_almacen', db.almacen, label="Almacén",
              requires=IS_IN_DB(db, 'almacen.id', '%(nombre)s', zero='Seleccione un almacén')),
        Field('cantidad', 'integer', label="Cantidad")
    )

    if form.process().accepted:
        # Aquí iría la lógica de crear el/los movimientos de transferencia
        try:
            result = insertar_movimiento(
                id_operativo=form.vars.operativo,
                id_almacen=form.vars.id_almacen,
                tipo_movimiento_txt=form.vars.id_tipo_movimiento,
                estatus_movimiento_txt=EST_MOV_VALIDADO,
                cantidad=form.vars.cantidad
            )
            
        except Exception as e:
            response.flash = f"Error al registrar la transferencia: {str(e)}"

        else:
            response.flash = 'Transferencia registrada correctamente.'

    elif form.errors:
        response.flash = f"Error en el formulario: {form.errors}"

    return dict(form=form)