from .schemas import UserSchema,ClientSchema,TriesSchema,LimitSchema
from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship, Api
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound
from flask import jsonify,request
from ..models import Client, Limits, User, UserTriesPerIdClient
from ..ext import db




# Create logical data abstraction (same as data storage for this first example)


class LimitDetail(ResourceDetail):
    def before_get_object(self,view_kwargs):
        if view_kwargs.get("id") is not None:
            try:  
                self.session.query(self.model).filter_by(id= view_kwargs["id"]).one()
            except NoResultFound:
                raise ObjectNotFound({"parameter":"id"},"{} {} not found".format(self.model.__tablename__,view_kwargs.get("id")))        
        if view_kwargs.get("id_client") is not None:
            try:
                client_=self.session.query(Client).filter_by(id=view_kwargs["id_client"]).one()
            except NoResultFound :
                raise ObjectNotFound({"parameter":"id_client"},"Client {} not found".format(view_kwargs.get("id_client")))
            else:
                if client_.limit is not None:
                    print("AQEUIIII")
                    view_kwargs["id"]=client_.id_limit
                else:
                    
                    raise ObjectNotFound({"parameter":"id"},"Doesn't have any Limit related")
    #revisar keywargs
    def before_marshmallow(self,args,kwargs):
        if request.method=="PATCH":
            key=[key for key,v in kwargs.items()][0]
            if key!="id":
                if kwargs.get(key) is not None:
                    try:
                        client_=self.data_layer["session"].query(Client).filter_by(id=kwargs[key]).one()
                    except NoResultFound:
                        raise ObjectNotFound({"parmeter":"id_client"},"Client {} not Found".format(kwargs[key]))
                    else:
                        if client_.id_limit:
                            kwargs["id"]=client_.id_limit 
                        else:
                            raise ObjectNotFound({"parameter: Object related"},"Doesnt exits any limit related")
        


    def after_get(self,result):
        return jsonify(result)

    schema=LimitSchema
    data_layer={
        "session":db.session,
        "model":Limits,
        "methods":{
                "after_get":after_get,
                "before_get_object":before_get_object,
                }
    }
class LimitList(ResourceList):

    def after_get(self,result):
            return jsonify(result)

    schema=LimitSchema
    data_layer={
    "session":db.session,
    "model":Limits,
    "methods":{
        "after_get":after_get
        }
    }
class LimitRelationship(ResourceRelationship):

    def after_get(self, result):
        return jsonify(result)

    schema=LimitSchema
    data_layer={
        "session":db.session,
        "model":Limits,
        "methods":{
        "after_get":after_get
        }
    }


class ClientDetail(ResourceDetail):
    def before_get_object(self, view_kwargs):
        if view_kwargs.get("id") is not None:
            try:
                self.session.query(self.model).filter_by(id= view_kwargs["id"]).one()
            except NoResultFound:
                raise ObjectNotFound({"parameter":"id"},"{} {} not found".format(self.model.__tablename__,view_kwargs.get("id")))
        if view_kwargs.get("tries_id") is not None:
            try:
                assc=self.session.query(UserTriesPerIdClient).filter_by(id=view_kwargs["tries_id"]).one()
            except NoResultFound :
                raise ObjectNotFound({"parameter":"tries_id"},"Client {} not found".format(view_kwargs.get("tries_id")))
            else:
                if assc.client is not None:
                    view_kwargs["id"]=assc.client.id
                else:
                    raise ObjectNotFound({"parameter":"tries_id"},"Doesn't have any Client related")
    def before_marshmallow(self,args,kwargs):
        if request.method=="PATCH":
            key=[key for key,v in kwargs.items()][0]
            if key!="id":
                if kwargs.get(key) is not None:
                    try:
                        assc=self.data_layer["session"].query(UserTriesPerIdClient).filter_by(id=kwargs[key]).one()
                    except NoResultFound:
                        raise ObjectNotFound({"parmeter":"tries_id"},"UserTriesPerIdClient {} not Found".format(kwargs[key]))
                    else:
                        if assc.id_client:
                            kwargs["id"]=assc.id_client
                        else:
                            raise ObjectNotFound({"parameter:Object related"},"Doesnt exits any Client related")

        

    def after_get(self,result):
        return jsonify(result)

    schema=ClientSchema
    data_layer={
        "session":db.session,
        "model":Client,
        "methods":{
            "after_get":after_get,
            "before_get_object":before_get_object
        }
    }
class ClientList(ResourceList):
    def query(self,view_kwargs):
        query_=self.session.query(Client)
        if view_kwargs.get("limit_id") is not None:
            try:
                self.session.query(Limits).filter_by(id=view_kwargs["limit_id"]).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'id'}, "Limits:{} not found".format(view_kwargs.get("limit_id")))
            else:
                query_=query_.filter(Client.id_limit == view_kwargs.get("limit_id"))
                # retornando query de los clientes relcionados con el limite especifiado por el id
        return query_
    def before_create_object(self,data, view_kwargs):
        if view_kwargs.get("limit_id") is not None:
            print(f"Limits CREATED DATA: {data}, VIEW_KWARGS:{view_kwargs}")
            try:
                limit_=self.session.query(Limits).filter_by(id=view_kwargs["limit_id"]).one() 
                data["id_limit"]=limit_.id
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'id'}, "Limits:{} not found".format(view_kwargs.get("limit_id")))

    def after_get(self,result):
            return jsonify(result)

    schema=ClientSchema
    data_layer={
        "session":db.session,
        "model":Client,
        "methods":{
            "query":query,
            "before_create_object":before_create_object,
            "after_get":after_get
        }
    }
class ClientRelationship(ResourceRelationship):

    def after_get(self, result):
        return jsonify(result)

    schema=ClientSchema
    data_layer={
        "session":db.session,
        "model":Client,
        "methods":{
        "after_get":after_get
        }
    }
class ClientUserRelationship(ResourceRelationship):

    def after_get(self, result):
        return jsonify(result)

    schema=ClientSchema
    data_layer={
        "session":db.session,
        "model":Client,
        "methods":{
            "after_get":after_get
        }
    }   



class TriesDetail(ResourceDetail):
    
    def before_get_object(self,view_kwargs):
        if view_kwargs.get("id") is not None:
            try:
                self.session.query(self.model).filter_by(id= view_kwargs["id"]).one()
            except NoResultFound:
                raise ObjectNotFound({"parameter":"id"},"{} {} not found".format(self.model.__tablename__,view_kwargs.get("id")))
    def after_get(self,result):
        return jsonify(result)

    schema=TriesSchema
    data_layer={
        "session":db.session,
        "model":UserTriesPerIdClient,
        "methods":{
            "after_get":after_get,
            "before_get_object":before_get_object
            }
    }
class TriesList(ResourceList):
    def query(self,view_kwargs):
        query_=self.session.query(self.model)
        if view_kwargs.get("id_client") is not None:
            arg="id_client"
            model=Client
        elif view_kwargs.get("id_user") is not None:
            arg="id_user"
            model=User
        else:
            arg=""
            model=None

        if view_kwargs.get(arg) is not None:
            try:
                self.session.query(model).filter_by(id=view_kwargs[arg]).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': arg}, "{}:{} not found".format(model.__tablename__,view_kwargs.get(arg)))
            else:
                query_=query_.join(model).filter(model.id==view_kwargs.get(arg))
                # retornando query de los usuarios relcionados con el rol especifiado por el id
        return query_

    def before_create_object(self,data, view_kwargs):
        if view_kwargs.get("id_client") is not None:
            arg="id_client"
            model=Client
        elif view_kwargs.get("id_user") is not None:
            arg="id_user"
            model=User
        else:
            arg=""
            model=None
        if view_kwargs.get(arg) is not None:
            print(f"CATEGORY CREATED DATA: {data}, VIEW_KWARGS:{view_kwargs}")
            try:
                model_=self.session.query(model).filter_by(id=view_kwargs[arg]).one() 
                data[arg]=model_.id
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'id'}, "{}:{} not found".format(model.__tablename__,view_kwargs.get("id_user")))
        print(data)
    def after_get(self,result):
            return jsonify(result)

    schema=TriesSchema
    data_layer={
        "session":db.session,
        "model":UserTriesPerIdClient,
        "methods":{
            "query":query,
            "before_create_object":before_create_object,
            "after_get":after_get
        }
    }
class TriesUserRelationship(ResourceRelationship):
    
    def after_get(self, result):
        return jsonify(result)

    schema=TriesSchema
    data_layer={
        "session":db.session,
        "model":UserTriesPerIdClient,
        "methods":{
            "after_get":after_get
            }
    }
class TriesClientRelationship(ResourceRelationship):

    def after_get(self, result):
        return jsonify(result)

    schema=TriesSchema
    data_layer={
        "session":db.session,
        "model":UserTriesPerIdClient,
        "methods":{
            "after_get":after_get
            }
    }

#GET POST PATCH DELETE relationship

class UserDetail(ResourceDetail):
    def before_get_object(self,view_kwargs):
        if view_kwargs.get("id") is not None:
            print("idddddddddddddd")
            try:  
                self.session.query(self.model).filter_by(id= view_kwargs["id"]).one()
            except NoResultFound:
                raise ObjectNotFound({"parameter":"id"},"{} {} not found".format(self.model.__tablename__,view_kwargs.get("id")))        
        if view_kwargs.get("tries_id") is not None:
            try:
                art=self.session.query(UserTriesPerIdClient).filter_by(id=view_kwargs["tries_id"]).one()
            except NoResultFound :
                raise ObjectNotFound({"parameter":"tries_id"},"UserTriesPerIdClient {} not found".format(view_kwargs.get("tries_id")))
            else:
                if art.id_user is not None:
                    print("AQEUIIII")
                    view_kwargs["id"]=art.id_user
                else:
                    
                    raise ObjectNotFound({"parameter":"id"},"Doesnt have any Category related")

    def before_marshmallow(self,args,kwargs):
        if request.method=="PATCH":
            print(f"kwargs:{kwargs}")
            key=[key for key,v in kwargs.items()][0]
            if key!="id":
                print("Key is not id")
                if kwargs.get(key) is not None:
                    try:
                        UserTriesPerIdClient_=self.data_layer["session"].query(UserTriesPerIdClient).filter_by(id=kwargs[key]).one()
                    except NoResultFound:
                        raise ObjectNotFound({"parmeter":"tries_id"},"UserTriesPerIdClient {} not Found".format(kwargs[key]))
                    else:
                        if UserTriesPerIdClient_.id_user:
                            kwargs["id"]=UserTriesPerIdClient_.id_user
                        else:
                            raise ObjectNotFound({"parameter: Object related"},"Doesnt exits any category related")
        


    def after_get(self,result):
        return jsonify(result)

    schema=UserSchema
    data_layer={
        "session":db.session,
        "model":User,
        "methods":{
                "after_get":after_get,
                "before_get_object":before_get_object,
                }
    }

class UserList(ResourceList):

    def after_get(self,result):
            return jsonify(result)

    schema=UserSchema
    data_layer={
    "session":db.session,
    "model":User,
    "methods":{
        "after_get":after_get
        }
    }
    
class UserClientRelationship(ResourceRelationship):

    def after_get(self, result):
        return jsonify(result)

    schema=UserSchema
    data_layer={
        "session":db.session,
        "model":User,
        "methods":{
        "after_get":after_get
        }
    }




