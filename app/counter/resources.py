from . import counter
from ..ext import db
from ..models import Limits, UserTries
from ..func import counter_func
from typing import Tuple


@counter.route("/counter/<int:user_id>/<int:client_id>", methods=["GET","POST"])
def counter_validation(user_id,client_id):
    result: Tuple[int, str] = counter_func(user_mapper=UserTries, 
                                            id_usuario=user_id,
                                            id_cliente=client_id,
                                            limits_mapper=Limits,
                                            db_object=db)
    print(f"result {result}")
    if result[0] == 0:
        return f"We are sorry, you just have exceeded your chances at this {result[1]} "
    else:
        return "process ..."

@counter.route("/addlimits", methods=["GET"])
def add_limits():
   data = {"id_cliente":1,"year":27,"month":9,"day":3}
   register = Limits(**data)
   db.session.add(register)
   db.session.commit()
   return "OK"
                                
