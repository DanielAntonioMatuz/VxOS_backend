from collections import namedtuple
from dataclasses import dataclass
from numbers import Real
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

db = SQLAlchemy()

@dataclass
class Users(db.Model):
    id: Integer = Column(Integer, primary_key=True)
    name: String = Column(String(1000))
    email: String = Column(String(1000))
    role: Integer = Column(Integer)  # NEW ATR
    password: String = Column(String(100))
    id_user_hash: Integer = Column(Integer)
    active: Boolean = Column(Boolean)
    accept_conditions_software: Boolean = Column(Boolean)
    created: TIMESTAMP = Column(TIMESTAMP)

@dataclass
class Licencia(db.Model):
    id: Integer = Column(Integer, primary_key=True)
    name: String = Column(String)
    price: Float = Column(Float)
    vigencia: String = Column(String)
    type: String = Column(String)
    marca: String = Column(String)
    estatus: String = Column(String)
    detalles_servicio: String = Column(String) # DETALLES SOBRE LA LICENCIA
    detalles_global: String = Column(String) # DETALLES SOBRE EL SERVICIO, SI ESTA ACTIVO O HAY ERRORES
    active: Boolean = Column(Boolean)

@dataclass
class User_licencia(db.Model):
    id: Integer = Column(Integer, primary_key=True)
    id_user: Integer = Column(Integer)
    id_licencia: Integer = Column(Integer)
    register: TIMESTAMP = Column(TIMESTAMP)
    expiration: TIMESTAMP = Column(TIMESTAMP)
    estatus: Integer = Column(Integer)
    compensacion: String = Column(String)


@dataclass
class Verification_user(db.Model):
    id: Integer = Column(Integer, primary_key=True)
    created: TIMESTAMP = Column(TIMESTAMP)
    email: String = Column(String)
    code: String = Column(String)


@dataclass
class Notifications(db.Model):
    id: Integer = Column(Integer, primary_key=True)
    title: String = Column(String)
    text: String = Column(String)
    footer: String = Column(String)
    css_color: String = Column(String)
    active: Boolean = Column(Boolean)
