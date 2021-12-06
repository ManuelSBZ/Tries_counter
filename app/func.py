
#LIMITES estan definidos en la tabla limits_mapper, por ahora se contempla 
#Dias,mes y año.

def counter_func(user_mapper, id_usuario, id_cliente, limits_mapper, db_object):

    import datetime

    #VALIDACION EXISTENCIA USUARIO SINO CREAR
    user_result = user_mapper.query.filter_by(id_user = id_usuario).first()
    print(f"user_result = {user_result}")

    if  user_result is None:
        print("NONE")
        data = {"day":0,"month":0,"year":0,"id_user":id_usuario}
        user_to_insert= user_mapper(**data)
        
        db_object.session.add(user_to_insert)
        db_object.session.commit()

        # reasignando registro para intentos de usuario
        user_result = user_mapper.query.filter_by(id_user = id_usuario).first()
    
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    current_day = datetime.datetime.now().day
    date_time_obj = user_result.date_reference
    # print(type(date_time_str))
    # date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

    # VERIFICANDO SI PASO AÑO,MES O DIA SI ES ASI: REINICIALIZAR LOS ELEMENTOS QUE APLIQUEN

    if current_year > date_time_obj.year :
        user_result.date_reference = datetime.datetime.now()
        user_result.day=0
        user_result.month=0
        user_result.year=0
        db_object.session.commit()

    elif current_month > date_time_obj.month:
        user_result.date_reference = datetime.datetime.now()
        user_result.day=0
        user_result.month=0
        db_object.session.commit()
    
    elif current_day > date_time_obj.day:
        user_result.date_reference = datetime.datetime.now()
        user_result.day = 0
        db_object.session.commit()
    
    #SECCION QUE VERIFICA NUMERO DE INTENTOS DEL USUARIO POR AÑO MES O DIA.
    print(f"id_cliente:{id_cliente}")
    limits = limits_mapper.query.filter_by(id_cliente = id_cliente).first()
    print(f"e {limits.__dict__}")

    if user_result.year >= limits.year:
        return (0, "year")
    if user_result.month >= limits.month:
        return (0, "month")
    if user_result.day >= limits.day:
        return (0, "day")

    user_result.year,user_result.month,user_result.day= (user_result.year+1,
                                                        user_result.month+1,
                                                        user_result.day+1)
    db_object.session.commit()
    return (1,"succesfully")

        
        


    

