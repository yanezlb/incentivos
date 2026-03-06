# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth
import os
import re

REQUIRED_WEB2PY_VERSION = "3.0.10"

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

web2py_version_string = request.global_settings.web2py_version.split("-")[0]
web2py_version = list(map(int, web2py_version_string.split(".")[:3]))
if web2py_version < list(map(int, REQUIRED_WEB2PY_VERSION.split(".")[:3])):
    raise HTTP(500, f"Requires web2py version {REQUIRED_WEB2PY_VERSION} or newer, not {web2py_version_string}")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if "GAE_APPLICATION" not in os.environ:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get("db.uri"),
             pool_size=configuration.get("db.pool_size"),
             migrate_enabled=configuration.get("db.migrate"),
             check_reserved=["all"])
else:
    # ---------------------------------------------------------------------
    # connect to Google Firestore
    # ---------------------------------------------------------------------
    db = DAL("firestore")
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be "controller/function.extension"
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get("app.production"):
    response.generic_patterns.append("*")

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = "bootstrap4_inline"
response.form_label_separator = ""

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = "concat,minify,inline"
# response.optimize_js = "concat,minify,inline"

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = "0.0.0"

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get("host.names"))
T.force('es')
T.accepted_date_format = '%Y-%m-%d'
T.accepted_datetime_format = '%Y-%m-%d %H:%M:%S'
IS_DATE.format = '%Y-%m-%d'

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------

db.define_table('ente',
    Field('nombre', 'string', label='Nombre', notnull=True, required=True),
    format='%(nombre)s'
)

db.define_table('negocio',
    Field('id_ente', db.ente, label='Ente', notnull=True, required=True),
    Field('nombre', 'string', label='Nombre', notnull=True, required=True),
    format='%(nombre)s'
)

db.define_table('localidad',
    Field('id_negocio', db.negocio, label='Negocio', notnull=True, required=True),  
    Field('nombre', 'string', label='Nombre', notnull=True, required=True),
    format='%(nombre)s'
)

db.define_table('region',
    Field('nombre', 'string', label='Nombre', notnull=True, required=True),
    format='%(nombre)s'
)

db.define_table('region_acopio',
    Field('nombre', 'string', label='Nombre', notnull=True, required=True),
    format='%(nombre)s'
)

db.define_table('estado',
    Field('id_region', db.region, label='Región', notnull=True, required=True),
    Field('id_region_acopio', db.region_acopio, label='Región de Acopio', notnull=True, required=True),
    Field('nombre', 'string', label='Nombre', notnull=True, required=True, requires=IS_UPPER(), compute=lambda r: r.nombre.upper()),
    Field('iso', 'string', label='ISO', notnull=True, required=True),
    format='%(nombre)s'
)
db.estado.nombre.represent = lambda value, row: value.upper() if value else ""

db.define_table('municipio',
    Field('id_estado', db.estado, label='Estado', notnull=True, required=True),
    Field('nombre', 'string', label='Nombre', notnull=True, required=True),
    format='%(nombre)s'
)
db.municipio.nombre.represent = lambda value, row: value.upper() if value else ""

db.define_table('parroquia',
    Field('id_municipio', db.municipio, label='Municipio', notnull=True, required=True),
    Field('nombre', 'string', label='Nombre', notnull=True, required=True),
    format='%(nombre)s'
)
db.parroquia.nombre.represent = lambda value, row: value.upper() if value else ""

auth.settings.extra_fields["auth_user"] = [
    Field('cedula', 'integer', label='CI'),
    Field('is_active','boolean', label='Estatus', default=True),
    Field('telefono', 'integer', label='Telf.'),
    Field('id_ente', db.ente, label='Ente', notnull=True, required=True),
    Field('id_negocio', db.negocio, label='Negocio / Filial', notnull=True, required=True),
    Field('id_region_acopio', db.region_acopio, label='Región Acopio', notnull=True, required=True),
    Field('id_estado', db.estado, label='Estado', notnull=True, required=True),
    Field('id_estado_acopio', db.estado, label='Estado Acopio', notnull=True, required=True),
    Field('fecha_nacimiento', 'date', label='Fecha de Nacimiento', requires=IS_DATE(format='%Y-%m-%d'), notnull=True, required=True),
    Field('fecha_ingreso', 'date', label='Fecha de Ingreso', requires=IS_DATE(format='%Y-%m-%d'), notnull=True, required=True),
]
auth.settings.logout_next = URL('default', 'user', args=['login'])

auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = "logging" if request.is_local else configuration.get("smtp.server")
mail.settings.sender = configuration.get("smtp.sender")
mail.settings.login = configuration.get("smtp.login")
mail.settings.tls = configuration.get("smtp.tls") or False
mail.settings.ssl = configuration.get("smtp.ssl") or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True


# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.actions_disabled = ['register', 'profile', 'change_password', 'request_reset_password', 'retrieve_username', 'retrieve_password']

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get("app.author")
response.meta.description = configuration.get("app.description")
response.meta.keywords = configuration.get("app.keywords")
response.meta.generator = configuration.get("app.generator")
response.show_toolbar = configuration.get("app.toolbar")

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get("google.analytics_id")

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get("scheduler.enabled"):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get("scheduler.heartbeat"))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table("mytable", Field("myfield", "string"))
#
# Fields can be "string","text","password","integer","double","boolean"
#       "date","time","datetime","blob","upload", "reference TABLENAME"
# There is an implicit "id integer autoincrement" field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield="value")
# >>> rows = db(db.mytable.myfield == "value").select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

# Funcion para el registro de campos para la auditoria en las tablas
db.auth_user.password.writable = False
db.auth_user.first_name.writable = False
db.auth_user.last_name.writable = False
db.auth_user.cedula.writable = False


def campos_comunes():
    campos_comunes = db.Table(db, 'comun',
        Field('creado_por',db.auth_user,default=auth.user_id,readable=False,writable=False),
        Field('fecha_reg','datetime',default=request.now,readable=False,writable=False),
        Field('fecha_mod','datetime',default=request.now,update=request.now,readable=False,writable=False),
        Field('modificado_por',db.auth_user,default=auth.user_id,readable=False,writable=False,update=auth.user_id),
        Field('ip_creado_por',default=request.env.REMOTE_ADDR,readable=False,writable=False),
        Field('ip_modificado_por',readable=False,writable=False,update=request.env.REMOTE_ADDR),
        Field('is_active','boolean', readable=False,writable=False,default=True),
    )
    return campos_comunes

db.define_table('tipo_almacen',
    Field('nombre', 'string', label='Nombre', notnull=True, required=True),
    format='%(nombre)s'
)

db.define_table('almacen',
    Field('id_region', db.region, label='Región', notnull=True, required=True),
    Field('id_region_acopio', db.region_acopio, label='Región de Acopio', notnull=True, required=True),
    Field('id_estado', db.estado, label='Estado', notnull=True, required=True),
    Field('id_municipio', db.municipio, label='Municipio', notnull=True, required=True),
    Field('id_parroquia', db.parroquia, label='Parroquia', notnull=True, required=True),
    Field('id_tipo_almacen', db.tipo_almacen, label='Tipo Almacen', notnull=True, required=True),
    Field('nombre', 'string', label='Nombre', notnull=True, required=True),
    Field('direccion', 'text', label='Dirección', notnull=True, required=True),
    campos_comunes()
)

db.define_table('estatus_operativo',
    Field('nombre', 'string', label='Nombre', notnull=True, required=True),
    format='%(nombre)s'
    )

db.define_table('operativo',
    Field('id_estatus_operativo', db.estatus_operativo, label='Estatus operativo', notnull=True, required=True, default=1),
    Field('fecha_inicio_solicitud', 'date', label='Fecha Inicio de Solicitud', notnull=True, required=True),
    Field('fecha_fin_solicitud', 'date', label='Fecha Fin de Solicitud', notnull=True, required=True),
    Field('fecha_inicio_entrega', 'date', label='Fecha Inicio de Entrega', notnull=True, required=True),
    Field('fecha_fin_entrega', 'date', label='Fecha Fin de Entrega', notnull=True, required=True),
    Field('nombre', 'string', label='Nombre del operativo', notnull=True, required=True, length=25),
    campos_comunes(),
    format='%(nombre)s'
)
db.operativo.fecha_inicio_solicitud.represent = lambda val, row: val.strftime('%Y-%m-%d') if val else ''
db.operativo.fecha_fin_solicitud.represent = lambda val, row: val.strftime('%Y-%m-%d') if val else ''
db.operativo.fecha_inicio_entrega.represent = lambda val, row: val.strftime('%Y-%m-%d') if val else ''
db.operativo.fecha_fin_entrega.represent = lambda val, row: val.strftime('%Y-%m-%d') if val else ''
db.operativo.fecha_inicio_solicitud.requires = IS_DATE(format='%Y-%m-%d')
db.operativo.fecha_fin_solicitud.requires = IS_DATE(format='%Y-%m-%d')
db.operativo.fecha_inicio_entrega.requires = IS_DATE(format='%Y-%m-%d')
db.operativo.fecha_fin_entrega.requires = IS_DATE(format='%Y-%m-%d')


db.define_table('operativo_combo',
    Field('id_operativo', db.operativo, label='Operativo', notnull=True, required=True),     
    Field('nombre', 'string', label='Nombre del combo', notnull=True, required=True, length=25),
    Field('cant_personas', 'integer', label='Cantidad de personas', notnull=True, required=True),
    Field('venta_maxima', 'integer', label='Entrega máxima', notnull=True, required=True),
    campos_comunes(),
    format='%(nombre)s'
)
db.operativo_combo.id_operativo.requires = [
    IS_IN_DB(db, 'operativo.id', '%(nombre)s', zero='Seleccione un operativo'), 
    IS_NOT_IN_DB(db, 'operativo_combo.id_operativo', error_message='Este operativo ya está asignado a otro combo')
]

db.define_table('pedido_operativo',
    Field('id_operativo', db.operativo, label='Operativo', notnull=True, required=True),     
    Field('id_operativo_combo',  db.operativo_combo, label='Combo', notnull=True, required=True),
    Field('id_usuario',  db.auth_user, label='Empleado', notnull=True, required=True),
    Field('estatus', 'list:string', label='Estatus Pedido', requires=IS_IN_SET(['REGISTRADO', 'ENTREGADO']), notnull=True, required=True),
    Field('observaciones', 'text', label='Observaciones'),
    campos_comunes()
)
db.pedido_operativo.estatus.represent = lambda valor, fila: XML(get_badge_estatus(valor))