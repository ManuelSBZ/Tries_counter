from . import counter
from ..ext import db
from ..models import User,Client,Limits,UserTriesPerIdClient
from ..func import counter_func_
from typing import Tuple
from ..classes import CounterBase


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
@counter.route("/counterbeta/<int:user_id>/<int:client_id>", methods=["GET","POST"])
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
                                
