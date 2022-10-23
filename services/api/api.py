# -------IMPORTING MODULES ------- #
import json
import secrets
from datetime import datetime
import pytz
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

from dao import Users, db, User_licencia, Licencia, Verification_user, Notifications

load_dotenv()

api = Blueprint('api', __name__)


@api.route('/get-licencias', methods=['GET'])
def get_licencias():
    response = {"body": "", "msg": "", "status_code": 200}
    try:
        id = request.args.get('id')
        licencias = User_licencia.query.filter_by(id_user=int(id)).all()

        arr_licencias = []
        notification = Notifications.query.filter_by(active=True).first()
        info_user = Users.query.filter_by(id=int(id)).first()
        all_licences = Licencia.query.all()
        for i in licencias:
            licencia_info = Licencia.query.filter_by(id=i.id_licencia).first()
            days_license = i.expiration - i.register
            arr_licencias.append({
                "compensacion": i.compensacion,
                "estatus": i.estatus,
                "id": i.id,
                "id_licencia": i.id_licencia,
                "expiration": i.expiration.strftime("%d/%m/%Y"),
                "dias_licencia_restante": days_license.days,
                "nombre_licencia": licencia_info.name,
                "detalles_global": licencia_info.detalles_global,
                "estatus_servicio": licencia_info.estatus
            })
        info_user.created = None
        response["body"] = arr_licencias
        info_user.password = None
        response["info_user"] = info_user
        response["licencias"] = all_licences
        response["notifications"] = notification
    except Exception as err:
        print(err)
        response["status_code"] = 400
        response["msg"] = str(err)
        return response, 400

    return response


@api.route('/validation-code', methods=['POST'])
def validation_code():
    response = {"body": False, "msg": "", "status_code": 200}
    try:
        req = request.json
        print(req)
        valid = Verification_user.query.filter_by(email=req['email'], code=req['code']).first()
        if valid:
            db.session.delete(valid)
            db.session.commit()
            response['body'] = True
    except Exception as err:
        print(err)
        response["status_code"] = 400
        response["msg"] = str(err)
        response['body'] = True
        return response, 400

    return response


@api.route('/restore-password', methods=['POST'])
def restore_password():
    response = {"body": "", "msg": "", "status_code": 200}
    try:
        req = request.json
        user = Users.query.filter_by(email=req['email']).first()
        user.password = generate_password_hash(req['password'], method='sha256')
        db.session.commit()
        response['body'] = 'Contraseña modificada'
        response['msg'] = True
    except Exception as err:
        print(err)
        response["status_code"] = 400
        response["msg"] = str(err)
        return response, 400

    return response