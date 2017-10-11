import sys

# handy to make mapper
from sqlalchemy import Column, ForeignKey, Integer, String
# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base
# to make foreginn key relationship
from sqlalchemy.orm import relationship
# for configuration code
from sqlalchemy import create_engine

# instance
Base = declarative_base()

# mapper
class Restaurant(Base):
    # table syntax
    # __tablename__ = 'some_table'
    __tablename__='restaurant'
    # columnName = Column(attribute,...)
    name = Column(String(80), nullable=False)
    restaurant_id = Column(Integer, primary_key=True)

class MenuItem(Base):
    __tablename__='menu_item'
    name = Column(String(80), nullable=False)
    menuItem_id = Column(Integer, primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.restaurant_id'))
    restauraunt = relationship(Restaurant)


engine = create_engine(
'sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine) 

