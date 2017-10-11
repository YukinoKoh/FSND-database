from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import from other py file
from database_setup import Base, Restaurant, MenuItem 

# which database to communicate
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
# create session maker object
DBSession = sessionmaker(bind=engine)
# session is to exceute, and commit
# 1: newEntry = ClassName(property='value')
# 2: sesion.add(newEntry)
# 3: session.commit()
session = DBSession()
# create data
restaurant1 = Restaurant(name="Riso's kitchen")
restaurant1_menu = MenuItem(name='Margarita')
restaurant1_menu.restaurant = restaurant1
# staging the data
session.add(restaurant1)
session.add(restaurant1_menu)
# store the data
session.commit()

