import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    email = Columne(String(250), nullable = False)

    @property
    def serialize(self):

        return{
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
 
class Category(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    items = relationship("Item")
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)

    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name
        }
 
class Item(Base):
    __tablename__ = 'item'


    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    category_id = Column(Integer,ForeignKey('category.id'))
    category = relationship(Category) 
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)

#We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
       
       return {
           'name'         : self.name,
           'description'         : self.description,
           'id'         : self.id,
       }
     



engine = create_engine('sqlite:///restaurantmenu.db')
 

Base.metadata.create_all(engine)