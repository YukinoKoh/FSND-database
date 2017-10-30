import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# instance
Base = declarative_base()

# mapper
class Category(Base):
    __tablename__='categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250), nullable=False)


class Tool(Base):
    __tablename__='tools'
    id = Column(Integer, primary_key=True)
    cat_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    name = Column(String(80), nullable=False)
    description = Column(String(250), nullable=False)
    image = Column(String(80))
    who = Column(String(250))
    preparation = Column(String(250))
    question = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return{
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'cat_id':self.cat_id
        }

class Link(Base):
    __tablename__='links'
    id = Column(Integer, primary_key=True)
    tool_id = Column(Integer, ForeignKey('tools.id'))
    title = Column(String(80), nullable=False)
    url = Column(String(250), nullable=False)
    source = Column(String(80))



engine = create_engine(
'sqlite:///researchtool.db')

Base.metadata.create_all(engine) 

