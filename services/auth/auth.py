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
from werkzeug.security import generate_password_hash, check_password_hash

from dao import Users, db

load_dotenv()

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    response = None

    try:
        req_data = request.get_json()
        print(req_data)
        user = Users.query.filter_by(email=req_data['email'], active=True).first()
        print(user)
        if not user or not check_password_hash(user.password, req_data['password']):
            return {
                'status_code': 404,
                'data': 'User not exist!'
            }
        user.password = ''
        response = {
            'user': {
                'id_user': user.id,
            },
            'secret-key': 'vxos'
        }
        data_user = {
            'id': user.id,
            'name': user.name,
            'active': True
        }
        access_token = create_access_token(
            identity=data_user,
            expires_delta=False
        )
        del response["secret-key"]
        response.update({
            "msg": "Process success",
            "access_token": access_token,
            "conditions": user.accept_conditions_software
        })
    except Exception as e:
        print(e)
    return {
        'status_code': 200,
        'data': response
    }


@auth.route('/signup', methods=['POST'])
def signup():
    req_data = request.get_json()
    response = None

    try:
        user = Users.query.filter_by(email=req_data['email']).first()
        if user:
            user.role = req_data['role']
            user.name = req_data['name']
            user.email = req_data['email']
            db.session.commit()
            return {
                'status_code': 200,
                'data': 'User already exist!'
            }

        new_user = Users(
            name=req_data['name'],
            email=req_data['email'],
            password=generate_password_hash(req_data['password'], method='sha256'),
            active=True,
            role=1,
            created=today(),
        )
        response = {
            'name': new_user.name,
            'email': new_user.email,
        }
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        print(e)

    return {
        'status_code': 200,
        'data': response
    }


@auth.route('/accept-conditions-software', methods=['POST'])
def accept_conditions_software():
    response = None

    try:
        req_data = request.get_json()
        print(req_data)

        user = Users.query.filter_by(id=int(req_data['id'])).first()
        user.accept_conditions_software = True
        db.session.commit()
    except Exception as e:
        print(e)
    print("9")
    return {
        'status_code': 200,
        'accept': True
    }

def today():
    format = "%Y-%m-%d %H:%M:%S %Z%z"
    now_utc = datetime.now(pytz.timezone('UTC'))
    now_mx = now_utc.astimezone(timezone('America/Mexico_City'))
    print(now_mx.strftime(format))
    return now_mx