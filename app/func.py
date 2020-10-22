
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
    
    #
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
    #tries
    if user_result.year >= limits.year:
        return (0, "year")
    if user_result.month >= limits.month:
        return (0, "month")
    if user_result.day >= limits.day:
        return (0, "day")
    #update
    user_result.year,user_result.month,user_result.day= (user_result.year+1,
                                                        user_result.month+1,
                                                        user_result.day+1)
    db_object.session.commit()
    return (1,"succesfully")

def counter_func_(id_user_mapper,
                        user_tries_mapper, 
                        id_usuario, 
                        id_cliente, 
                        limits_mapper, 
                        id_client_mapper,
                        db_object):

    import datetime

    #VALIDACION EXISTENCIA USUARIO SINO CREAR
    user_result = id_user_mapper.query.filter_by(id_user = id_usuario).first()
    
    object_client = id_client_mapper.query.filter_by(id_client=id_cliente).first()

    if object_client is None:
        print("please you must to fill the table client and relate it to a limit")
        return "please you must to fill the table client and relate it to a limit"
        
    if user_result is None:
        print("User result : NONE")
        # insertando nuevo usuario en User
        data_user = {"id_user":id_usuario}
        user_to_insert = id_user_mapper(**data_user)
        db_object.session.add(user_to_insert)
        db_object.session.commit() 
        #recuperando objeto cliente para relacionarlo a User mediante UserTriesPerIdClient
        data_user_tries = {"day":0,
                           "month":0,
                           "year":0,
                           "id_user":user_to_insert.id,
                           "id_client":object_client.id}
        user_tries_to_insert= user_tries_mapper(**data_user_tries)
            
        db_object.session.add(user_tries_to_insert)
        db_object.session.commit()

    # recuperando registro de user_tries
    user_tries_result = user_tries_mapper.query.filter_by(id_user = user_result.id, 
                                                          id_client= object_client.id).first()
    print(f"user_tries_result : {user_tries_result}")
    if user_tries_result is None:
        data_user_tries = {"day":0,
                           "month":0,
                           "year":0,
                           "id_user":user_result.id,
                           "id_client":object_client.id}

        user_tries_to_insert = user_tries_mapper(**data_user_tries)
        user_tries_result =  user_tries_to_insert          
        db_object.session.add(user_tries_to_insert)
        db_object.session.commit()


    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    current_day = datetime.datetime.now().day
    date_time_obj = user_tries_result.date_reference
    # print(type(date_time_str))
    # date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

    # VERIFICANDO SI PASO AÑO,MES O DIA SI ES ASI: REINICIALIZAR LOS ELEMENTOS QUE APLIQUEN

    if current_year > date_time_obj.year :
        user_tries_result.date_reference = datetime.datetime.now()
        user_tries_result.day=0
        user_tries_result.month=0
        user_tries_result.year=0
        db_object.session.commit()

    elif current_month > date_time_obj.month:
        user_tries_result.date_reference = datetime.datetime.now()
        user_tries_result.day=0
        user_tries_result.month=0
        db_object.session.commit()
    
    elif current_day > date_time_obj.day:
        user_tries_result.date_reference = datetime.datetime.now()
        user_tries_result.day = 0
        db_object.session.commit()

   #SECCION QUE VERIFICA NUMERO DE INTENTOS DEL USUARIO POR AÑO MES O DIA.
    print(f"id_cliente:{object_client.id}") 
    limits = limits_mapper.query.filter_by(id=object_client.id_limit).first()
    print(f"e {limits.__dict__}")
    #tries
    if user_tries_result.year >= limits.year:
        return (0, "year")
    if user_tries_result.month >= limits.month:
        return (0, "month")
    if user_tries_result.day >= limits.day:
        return (0, "day")
    #update
    user_tries_result.year,user_tries_result.month,user_tries_result.day= (user_tries_result.year+1,
                                                        user_tries_result.month+1,
                                                        user_tries_result.day+1)
    db_object.session.commit()
    return (1,"succesfully")
        
                