from . import counter
from ..ext import db, redis_connection as r
from ..models import User,Client,Limits,UserTriesPerIdClient
from ..func import counter_func_
from typing import Tuple
from flask import request


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

# @counter.route("/addlimits", methods=["GET"])
# def add_limits():
#    data = {"id_cliente":1,"year":27,"month":9,"day":3}
#    register = Limits(**data)
#    db.session.add(register)
#    db.session.commit()
#    return "OK"
@counter.route("/addtoredis", methods = ["GET","POST"])
def add_redis():
    size_query = len(list(request.args.keys()))
    aux = request.args
    print(aux)
    if size_query != 0:
        query_string = request.args
        print(query_string)
        return query_string
    return "ok nothing"

@counter.route("/redis", methods = ["GET","POST"])
def addtoredis():
    query = reques.args

    r.mset({"Croatia": "Zagreb", "Bahamas": "prusia"})

    city = r.get("Bahamas")

    return city
        
        

                                
