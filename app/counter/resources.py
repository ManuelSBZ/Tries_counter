from . import counter
from ..ext import db
from ..models import User,Client,Limits,UserTriesPerIdClient,Owner
from ..func import counter_func_, token_required
from typing import Tuple
from ..classes import CounterBase
from flask import jsonify, request, current_app, make_response
from werkzeug.security import check_password_hash,generate_password_hash 
import uuid
import jwt



@counter.route("/counter/<int:user_id>/<int:client_id>", methods=["GET","POST"])
def counter_validation(user_id,client_id):
    result: Tuple[int, str] = counter_func_(id_user_mapper=User,
                                            user_tries_mapper=UserTriesPerIdClient,
                                            id_cliente=client_id,
                                            id_usuario=user_id,
                                            limits_mapper=Limits,
                                            id_client_mapper=Client,
                                            db_object=db)
    print(f"result {result}")
    if result[0] == 0:
        return f"We are sorry, you just have exceeded your chances at this {result[1]} "
    else:
        return "process continuation ..."

@counter.route("/counterbeta/<int:user_id>/<int:client_id>", methods=["GET","POST"])
@token_required
def counter_validation_beta(user_id,client_id):
    counter = CounterBase(user_model=User,
                          tries_model=UserTriesPerIdClient,
                          id_usuario=user_id,
                          id_cliente=client_id,
                          limits_model=Limits,
                          client_model=Client,
                          db_object=db)
    counter.check_and_create()
    counter.verify_time_elapsed()
    result: Tuple[int, str] = counter.are_limits_exceded()
    print(f"result {result}")
    if result[0] == 0:
        return f"We are sorry, you just have exceeded your chances at this {result[1]} "
    else:
        return "process continuation ..."

@counter.route("/counterbetaday/<int:user_id>/<int:client_id>", methods=["GET","POST"])
def counter_validation_beta_per_day(user_id,client_id):
    counter = CounterBase(user_model=User,
                          tries_model=UserTriesPerIdClient,
                          id_usuario=user_id,
                          id_cliente=client_id,
                          limits_model=Limits,
                          client_model=Client,
                          db_object=db)
    counter.check_and_create()
    counter.verify_time_elapsed(per_day=True)
    result: Tuple[int, str] = counter.are_limits_exceded()
    print(f"result {result}")
    if result[0] == 0:
        return f"We are sorry, you just have exceeded your chances at this {result[1]} "
    else:
        return "process continuation ..."
                                
@counter.route('/register', methods=['GET', 'POST'])
def signup_owner():
    data = request.get_json()
    if not data.get("password") and not data.get("name"):
        return jsonify({'message':'keys should be "password" and "name" ',"status":"400"})
    password = data['password']
    new_user = Owner(public_id=str(uuid.uuid4()), name=data['name'], password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'registered successfully'})

@counter.route('/getToken', methods=['GET', 'POST'])
def login_user():
    import datetime
    auth = request.authorization
    print(f"not auth or not auth.username or not auth.password : {not auth or not auth.username or not auth.password}")
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
    
    owner = Owner.query.filter_by(name=auth.username).first()
    if owner is None: return jsonify({"message":"user doesn't exist"})
    print(f"check_password_hash(owner.password_hash, auth.password): {check_password_hash(owner.password_hash, auth.password)}, hash:{owner.password_hash}, hash_type:{type(owner.password_hash)}, password:{auth.password}, password:{type(auth.password)}")
    if check_password_hash(owner.password_hash, auth.password):
        token = jwt.encode({'public_id': owner.public_id, 
                            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=1)}, 
                            current_app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

@counter.route('/prueba', methods=['GET', 'POST'])
@token_required
def prueba(current_user):
    print(current_user.__dict__)
    return "niceeee"