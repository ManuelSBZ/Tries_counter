from sqlalchemy import String,Integer,Boolean,Float,ForeignKey, Column,  DateTime
from sqlalchemy.orm import relationship
from .ext import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class User(db.Model):
    #cantidades actuales de intentos por usuario
    __tablename__='User'
    #Primary key como atributo
    id = Column(Integer, primary_key=True, nullable=False)
    id_user = Column(Integer, nullable=False)
    client_association = relationship("UserTriesPerIdClient", back_populates="user")

class Client(db.Model):
    __tablename__='Client'
    id = Column(Integer, primary_key=True, nullable=False)
    id_client = Column(Integer, nullable=False)
    id_limit = Column(Integer, ForeignKey("Limits.id"))
    user_association = relationship("UserTriesPerIdClient", back_populates="client")

class UserTriesPerIdClient(db.Model):
    __tablename__='UserTriesPerIdClient'
    id = Column(Integer(), primary_key=True , nullable=False)
    id_user = Column(Integer, ForeignKey('User.id'))
    id_client = Column(Integer, ForeignKey("Client.id"))
    day = Column(Integer,default=1, nullable=False)
    month = Column(Integer,default=1, nullable=False)
    year = Column(Integer,default=1, nullable=False)
    date_reference = Column(DateTime, nullable=False, default=datetime.datetime.now()) 
    user = relationship("User", back_populates="client_association")
    client = relationship("Client", back_populates="user_association")

class Limits(db.Model):
    #cantidades maximas de intentos
    __tablename__="Limits"
    id=Column(Integer, primary_key=True, nullable=False)
    id_client=relationship("Client", backref="limit", lazy=True)
    day=Column(Integer,default=3, nullable=False)
    month=Column(Integer,default=9, nullable=False)
    year=Column(Integer,default=27, nullable=False)



