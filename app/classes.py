import datetime
from sqlalchemy.orm.exc import NoResultFound
class CounterBase:
    def __init__(self, user_model, tries_model, 
                                id_usuario, 
                                id_cliente, 
                                limits_model, 
                                client_model,
                                db_object):

        self.user_model = user_model
        self.tries_model = tries_model 
        self.id_usuario = id_usuario
        self.id_cliente = id_cliente 
        self.limits_model = limits_model
        self.client_model = client_model 
        self.db_object = db_object
    


    def check_and_create(self):
        if type(self.id_usuario) is not int: raise TypeError("Type must be an int")
        if type(self.id_cliente) is not int : raise TypeError("Type must be an int")
        print(f"este es el asqueroso self.id_usuario : {self.id_usuario}")
        user_result = self.user_model.query.filter_by(id_user = self.id_usuario).first()
        client_result = self.client_model.query.filter_by(id_client = self.id_cliente).first()
        if client_result is None:
            raise NoResultFound(
                    "client is None, must be created with an associated limit")
        self.client_result=client_result
        if user_result is None:
            data_user = {"id_user":self.id_usuario}
            user_to_insert = self.user_model(**data_user)
            user_result=user_to_insert
            self.db_object.session.add(user_to_insert)
            self.db_object.session.commit()
        self.user_result = user_result 
        self.tries_result = self.tries_model.query.filter_by(id_client=self.client_result.id, 
                                                  id_user = self.user_result.id).first()
        if self.tries_result is None:
            print("TRIES NONE")
            data_user_tries = {"day":0,
                                "month":0,
                                "year":0,
                                "id_user":user_result.id,
                                "id_client":client_result.id}

            user_tries_to_insert = self.tries_model(**data_user_tries)         
            self.db_object.session.add(user_tries_to_insert)
            self.db_object.session.commit()
            self.tries_result = user_tries_to_insert          

    def verify_time_elapsed(self,per_day=False):
        # try:
        #     print(self.id_usuario, self.id_cliente)
        #     tries_result = self.tries_model.query.filter_by(id_client=self.client_result.id, 
        #                                 id_user = self.user_result.id).first()
        #     print(tries_result)
        #     date_reference = tries_result.date_reference
        # except (NoResultFound,AttributeError) as error:
        #     raise Exception(error)

        if per_day:
            current_date = datetime.datetime.now()
            delta = current_date - self.tries_result.date_reference
            print(f"deltadays:{delta.days}")
            status = {"year":(delta.days>=365)
                     ,"month":(delta.days>=30)
                     ,"day":(delta.days>=1)}
        else:    
            currentyear = datetime.datetime.now().year
            currentmonth = datetime.datetime.now().month
            currentday = datetime.datetime.now().day
            status={"year":(currentyear>self.tries_result.date_reference.year)
                    ,"month":(
                        currentmonth>self.tries_result.date_reference.month
                        )
                    ,"day":(currentday>self.tries_result.date_reference.day)}        

        if status["year"]:
            self.tries_result.date_reference = datetime.datetime.now()
            self.tries_result.day=0
            self.tries_result.month=0
            self.tries_result.year=0
            self.db_object.session.commit()

        elif status["month"]:
            self.tries_result.date_reference = datetime.datetime.now()
            self.tries_result.day=0
            self.tries_result.month=0
            self.db_object.session.commit()
        
        elif status["day"]:
            self.tries_result.date_reference = datetime.datetime.now()
            self.tries_result.day = 0
            self.db_object.session.commit()

    def are_limits_exceded(self):
        limits = self.limits_model.query.filter_by(
                                    id=self.client_result.id_limit).first()
        if limits is None:
            raise NoResultFound(
                    "limit is None, must be created with an associated client")

        print(f"e {limits.__dict__}")
        #tries
        if self.tries_result.year >= limits.year:
            return (0, "year")
        if self.tries_result.month >= limits.month:
            return (0, "month")
        if self.tries_result.day >= limits.day:
            return (0, "day")
        #update
        self.tries_result.year,self.tries_result.month,self.tries_result.day = (
                                                     self.tries_result.year+1,
                                                     self.tries_result.month+1,
                                                     self.tries_result.day+1)
        self.db_object.session.commit()
        return (1,"succesfully")
                                
# class CounterSchedule(CounterBase):
#     def init(self, user_model, tries_model, 
#                                  id_usuario, 
#                                  id_cliente, 
#                                 limits_model, 
#                                 client_model,
#                                 db_object):
#         CounterBase.__init__(self,user_model,
#                              tries_model, 
#                              id_usuario, 
#                              id_cliente, 
#                              limits_model, 
#                              client_model, 
#                              db_object)
#     def verify_time_elapsed(self):
        


