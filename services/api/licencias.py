# -------IMPORTING MODULES ------- #
import json
from datetime import datetime
import pytz
from pytz import timezone

import requests
from dotenv import load_dotenv
# from api_functions_external import *
from flask import (
    request,
    Blueprint
)
from flask_jwt_extended import (
    create_access_token,
)
from services.auth.auth import today
from werkzeug.security import generate_password_hash, check_password_hash

from dao import Users, db, User_licencia, Licencia

load_dotenv()

licence = Blueprint('licence', __name__)


@licence.route('/register-licence', methods=['POST'])
def register_licence():
    response = {"body": "", "msg": "", "status_code": 200}
    data = request.json
    valid_license = Licencia.query.filter_by(name=data['name']).first()
    try:
        if valid_license is None:
            new_licence = Licencia(
                name=data['name'],
                price=int(data['price']),
                vigencia=data['vigencia'],
                type=data['type'],
                marca=data['marca'],
                estatus=data['estatus'],
                detalles_servicio=data['detalles_servicio'],
                detalles_global=data['detalles_global'],
                active=True
            )
            db.session.add(new_licence)
            db.session.commit()
        else:
            response['msg'] = 'Licencia ya existe.'
    except Exception as err:
        print(err)

    return response


@licence.route('/register-licence-to-user', methods=['POST'])
def register_licence_to_user():
    response = {"body": "", "msg": "", "status_code": 200}
    data = request.json
    valid_license = User_licencia.query.filter_by(id_licencia=data['id_licencia'], id_user=int(data['id_user'])).first()
    try:
        if valid_license is None:
            expiration = add_years(today(), 1)
            print('expiration', expiration)
            new_licence = User_licencia(
                id_user=int(data['id_user']),
                id_licencia=data['id_licencia'],
                register=today(),
                expiration=expiration,
                estatus=1,
                compensacion=data['compensacion']
            )
            db.session.add(new_licence)
            db.session.commit()
        else:
            valid_license.estatus = int(data['estatus']),
            valid_license.compensacion = data['compensacion']
            db.session.commit()
    except Exception as err:
        print(err)

    return response


def add_years(start_date, years):
    try:
        return start_date.replace(year=start_date.year + years)
    except ValueError:
        return start_date.replace(year=start_date.year + years)
