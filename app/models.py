from sqlalchemy import String,Integer,Boolean,Float,ForeignKey, Column,  DateTime
from sqlalchemy.orm import relationship
from .ext import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class UserTries(db.Model):
    #cantidades actuales de intentos por usuario
    __tablename__='UserTries'
    #Primary key como atributo
    id=Column(Integer, primary_key=True, nullable=False)
    id_user = Column(Integer, nullable=False)
    day=Column(Integer,default=1, nullable=False)
    month=Column(Integer,default=1, nullable=False)
    year=Column(Integer,default=1, nullable=False)
    date_reference = Column(DateTime, nullable=False, default=datetime.datetime.now()) 

class Limits(db.Model):
    #cantidades maximas de intentos
    __tablename__="Limits"
    id=Column(Integer, primary_key=True, nullable=False)
    id_cliente=Column(Integer, nullable=False)
    day=Column(Integer,default=3, nullable=False)
    month=Column(Integer,default=9, nullable=False)
    year=Column(Integer,default=27, nullable=False)
