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
# create restaurants data
restaurant1 = Restaurant(name="Rico's kitchen")
restaurant2 = Restaurant(name="Groument Burger")
session.add(restaurant1)
session.add(restaurant2)
session.commit()

# create menu data
menu1_plus = session.query(MenuItem).first() 
menu1 = MenuItem(name='Margarita')
menu2 = MenuItem(name='Pepper pizza')
menu3 = MenuItem(name="Today's pasta")
menu4 = MenuItem(name='Groumet Special')
menu5 = MenuItem(name='Organic burger')
menu6 = MenuItem(name='Seasonal burger')
menu1.restaurant_id =  session.query(Restaurant).filter_by(id=1).one().id
menu2.restaurant_id =  session.query(Restaurant).filter_by(id=1).one().id
menu3.restaurant_id =  session.query(Restaurant).filter_by(id=1).one().id
menu4.restaurant_id =  session.query(Restaurant).filter_by(id=2).one().id
menu5.restaurant_id =  session.query(Restaurant).filter_by(id=2).one().id
menu6.restaurant_id =  session.query(Restaurant).filter_by(id=2).one().id
menu1.price = '$3.29'
menu2.price = '$2.29'
menu3.price = '$1.29'
menu4.price = '$3.79'
menu5.price = '$2.79'
menu6.price = '$1.79'
session.add(menu1)
session.add(menu2)
session.add(menu3)
session.add(menu4)
session.add(menu5)
session.add(menu6)
session.commit()


