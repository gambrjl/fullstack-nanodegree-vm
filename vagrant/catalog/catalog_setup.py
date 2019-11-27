#!/usr/bin/env python

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):

        return {
            'id'        : self.id,
            'name'      : self.name,
            'email'     : self.email,
            'picture'   : self.picture,
        }

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    category_name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)

    @property
    def serialize(self):
       
       return {
           'id'     : self.id,
           'category_name'   : self.category_name,
           'user_id'        : self.user_id
       }

class CategoryItems(Base):
    __tablename__ = 'category_item'

    id = Column(Integer, primary_key = True)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)

    @property
    def serialize(self):

        return {
            'name'      : self.name,
            'description'   : self.description,
            'category_id'   : self.category_id,
            'id'            : self.id,
            'user_id'       : self.user_id

        }

engine = create_engine('sqlite:///items.db')

Base.metadata.create_all(engine)
