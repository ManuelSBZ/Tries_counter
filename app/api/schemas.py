

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship,Schema

class LimitSchema(Schema):
    class Meta:
        type_ = 'limit'
        self_view = 'api_v1.limit_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api_v1.limit_list'

    id = fields.Integer(as_string=True, dump_only=True)
    day = fields.Integer()
    month = fields.Integer()
    year = fields.Integer()
    clients = Relationship(self_view='api_v1.limit_clients',
                             self_view_kwargs={'id': '<id>'},
                             related_view='api_v1.client_list',
                             related_view_kwargs={'limit_id': '<id>'},
                             many=True,
                             schema='ClientSchema',
                             type_='client',
                             attribute='client')

class ClientSchema(Schema):
    class Meta:
        type_ = 'client'
        self_view = 'api_v1.client_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api_v1.client_list'

    id = fields.Integer(as_string=True, dump_only=True)
    id_client = fields.Integer(required=True)
    id_limit = fields.Integer()
    limit = Relationship(   self_view='api_v1.client_limit',
                            self_view_kwargs={'id': '<id>'},
                            related_view='api_v1.limit_detail',
                            related_view_kwargs={'id_client': '<id>'},
                            schema='LimitSchema',
                            type_='limit'
                            )
    tries_association=Relationship(
                            attribute = "user_association",
                            self_view="api_v1.client_asso",
                            self_view_kwargs={"id":"<id>"},
                            related_view="api_v1.tries_list",
                            related_view_kwargs={"id_client":"<id>"},
                            schema="TriesSchema",
                            type_="tries"
                        )

class TriesSchema(Schema):
    class Meta:
        type_ = 'tries'
        self_view = 'api_v1.tries_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api_v1.tries_list'

    id = fields.Integer(as_string=True, dump_only=True)
    id_user = fields.Integer()
    id_client = fields.Integer()
    day = fields.Integer()
    month = fields.Integer()
    year = fields.Integer()
    date_reference = fields.Date() 
    user=Relationship(
        self_view="api_v1.tries_user",
        self_view_kwargs={"id":"<id>"},
        related_view="api_v1.user_detail",
        related_view_kwargs={"tries_id":"<id>"},
        schema="UserSchema",
        type_="user"
    )
    client = Relationship(
        self_view="api_v1.tries_client",
        self_view_kwargs={"id":"<id>"},
        related_view="api_v1.client_detail",
        related_view_kwargs={"tries_id":"<id>"},
        schema="ClientSchema",
        type_="client"
    )

class UserSchema(Schema):
    class Meta:
        type_ = 'user'
        self_view = 'api_v1.user_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api_v1.user_list'

    id = fields.Integer(as_string=True, dump_only=True)
    id_user = fields.Integer()
    tries = Relationship(
                            attribute="client_association",
                            self_view="api_v1.user_asso",
                            self_view_kwargs={"id":"<id>"},
                            related_view="api_v1.tries_list",
                            related_view_kwargs={"id_user":"<id>"},
                            schema="TriesSchema",
                            type_="tries"
                        )
