import os
import secrets

from dao import db, Users, Verification_user
from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail, Message
from services.api.licencias import licence

from services.auth.auth import auth, today
from services.api.api import api

app = Flask(__name__)

app.register_blueprint(auth)
app.register_blueprint(api)
app.register_blueprint(licence)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_POOL_SIZE'] = 700
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("VXOS_CONNECTION")


# SERVER EMAIL CONFIGURATION CREDENTIALS
app.config['MAIL_SERVER'] = 'smtp.ionos.mx'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'dm@vxos.com.mx'
app.config['MAIL_PASSWORD'] = 'Kirasonata1'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)


@app.route('/')
def hello_world():  # put application's code here
    return {
        'status_code': 200,
        'api_version': '1.0.0',
        'release_productive': True,
        'project': 'VxOS',
        'designed_by': 'VxOS'
    }


@app.route('/email-support', methods=['POST'])
def send_support():
    data = {"status_code": 200, "data": "", "msg": "Proceso concluido correctamente", "ok": True}
    try:
        req = request.json
        print(req)
        user = Users.query.filter_by(id=int(req['id_user'])).first()
        msg = Message('SOLICITUD DE SOPORTE:: ' + user.email,
                      sender='dm@vxos.com.mx', recipients=["portal@vxos.com.mx"])
        msg.body = req['mensaje']

        mail.send(msg)
    except Exception as e:
        print(e)
        data = {"status_code": 500, "data": "", "msg": "Ah ocurrido un error durante el proceso, intente mas tarde.",
                "ok": False}
    return data


@app.route('/buy-license', methods=['POST'])
def send_buy_license():
    data = {"status_code": 200, "data": "", "msg": "Proceso concluido correctamente", "ok": True}
    try:
        req = request.json
        print(req)
        user = Users.query.filter_by(id=int(req['id_user'])).first()
        msg = Message('SOLICITUD DE COMPRA:: ' + user.email,
                      sender='dm@vxos.com.mx', recipients=["portal@vxos.com.mx"])
        msg.body = 'SOLICITUD DE COMPRA DEL CLIENTE: {}, para una licencia de tipo: {}, al email: {}, ' \
                   'con método de pago: {}'.format(user.email, req['tipo_licencia'], req['email_licencia'], req['metodo_pago'])

        mail.send(msg)
    except Exception as e:
        print(e)
        data = {"status_code": 500, "data": "", "msg": "Ah ocurrido un error durante el proceso, intente mas tarde.",
                "ok": False}
    return data


@app.route('/send-code', methods=['GET'])
def send_code_verification():
    data = {"status_code": 200, "data": "", "msg": "Proceso concluido correctamente", "ok": True}
    try:
        email = request.args.get('email')
        user = Verification_user.query.filter_by(email=email).first()
        if user is not None:
            db.session.delete(user)
            db.session.commit()
        code_auth = secrets.randbelow(9000)
        code_auth = str(code_auth).zfill(4)
        new_code = Verification_user(
            created=today(),
            email=email,
            code=code_auth
        )
        db.session.add(new_code)
        db.session.commit()
        msg = Message('Codigo de seguridad:: ' + email,
                      sender='dm@vxos.com.mx', recipients=[email])
        msg.body = 'Tu código de seguridad para cambiar tu contraseña es {}'.format(code_auth)

        mail.send(msg)
    except Exception as e:
        print(e)
        data = {"status_code": 500, "data": "", "msg": "Ah ocurrido un error durante el proceso, intente mas tarde.",
                "ok": False}
    return data


db.init_app(app)
jwt = JWTManager(app)
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
