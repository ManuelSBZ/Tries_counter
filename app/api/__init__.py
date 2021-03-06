from flask import Blueprint
from ..ext import api
from .resources import *

print(f"NOMBRE:{__name__}")
api_v1 = Blueprint("api_v1", __name__+"_v1", url_prefix="/api")

api.route(LimitList, 'limit_list', '/limits')
api.route(LimitDetail, 'limit_detail', '/limits/<int:id>', '/clients/<int:id_client>/limit')
api.route(LimitRelationship, 'limit_clients', '/limits/<int:id>/relationships/clients')

api.route(ClientList, 'client_list', '/clients', '/limits/<int:limit_id>/clients')
api.route(ClientDetail, 'client_detail', '/clients/<int:id>', '/tries/<int:tries_id>/client')
api.route(ClientRelationship, 'client_limit', '/clients/<int:id>/relationships/limit')
api.route(ClientUserRelationship, 'client_asso', '/clients/<int:id>/relationships/tries')

api.route(TriesDetail,"tries_detail","/tries/<int:id>")# GET PATCH DELETE ORDER_ARTICLE ASSOCIATION

api.route(TriesList, "tries_list", 
         "/tries", 
         "/users/<int:id_user>/tries", 
         "/clients/<int:id_client>/tries")##GET POST ARTICLE_ASSOCIATION, POST ORDER_ARTICLE => ORDER, POST ORDER_ARTICLE => ARTICLE

api.route(TriesUserRelationship, "tries_user", "/tries/<int:id>/relationship/user")#GET POST PATCH DELETE relationship

api.route(TriesClientRelationship, "tries_client", "/tries/<int:id>/relationship/client")

api.route(UserList, 'user_list', '/users')
api.route(UserDetail, 'user_detail', '/users/<int:id>', '/tries/<int:tries_id>/user')
api.route(UserClientRelationship, 'user_asso', '/users/<int:id>/relationship/tries')
