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
myFirstRestaurant = Restaurant(name='PizzaStore')
myFirstMenu = MenuItem(name='Margarita')
# staging the data
session.add(myFirstRestaurant)
session.add(myFirstMenu)
# store the data
session.commit()

# query the data
result =  session.query(Restaurant).first()
print result.name

# select
margaritas = session.query(MenuItem).filter_by(name='Margarita')
for margarita in margaritas:
    print margarita.menuItem_id
    print '\n'

# update 
firstMargarita = session.query(MenuItem).filter_by(name='Margarita').one()
firstMargarita.price = '$2.99'
session.add(firstMargarita)
session.commit()

print session.query(MenuItem).filter_by(name='Margarita').one().price
session.commit()
