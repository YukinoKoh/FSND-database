from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import from other py file
from database_setup import Base, Category, Tool, Link 

# which database to communicate
engine = create_engine('sqlite:///researchtool.db')
Base.metadata.bind = engine
# create session maker object
DBSession = sessionmaker(bind=engine)
# session is to exceute, and commit
session = DBSession()

# create category data
cat1 = Category(name="Exploratory",
                description="It is for a project in new area that requires explorative research to find potential of the project.")
cat2 = Category(name="Fundamental",
                description="It is to understand users for better decision through the project process.")
cat3 = Category(name="Generative",
                description="It is to Generate ideas with shared insights, which gained through iterative refinement.")
cat4 = Category(name="Communicative",
                description="It is to draw back stories to communicate internal and external stakeholders.")
cat5 = Category(name="Evaluative",
                description="""It is to evaluate ideas across its usage based on 
                            the fundamental research, involving users and engineers.""") 
cat6 = Category(name="Applicative",
                description="It is to share, refine and apply the product vision, involving key team members.") 
session.add(cat1)
session.add(cat2)
session.add(cat3)
session.add(cat4)
session.add(cat5)
session.add(cat6)
session.commit()

# create tools data
tool1 = Tool(name='User Journey', cat_id=2,
             description="It is to draw touch points, by behavior of a hypothesized group of users.")
tool2 = Tool(name='Persona', cat_id=2,
             description="It is to understand personality of a hypothesized group of users.")
tool3 = Tool(name='Empathy Map', cat_id=2,
             description="It is to gain insight about users, developing empathy for other people.")
tool4 = Tool(name='Mind map', cat_id=3,
             description="It is to understand touch points.")
tool5 = Tool(name='Usability Test', cat_id=5,
             description="It is to identify further improvement of the product.")
session.add(tool1)
session.add(tool2)
session.add(tool3)
session.add(tool4)
session.add(tool5)
session.commit()

# create link data
link1 = Link(title='Updated Empathy Map Canvas', tool_id=3, source='Medium',
             url='https://medium.com/the-xplane-collection/updated-empathy-map-canvas-46df22df3c8a')
link2 = Link(title='Usability Testing', tool_id=5, source='usability.gov',
             url='https://www.usability.gov/how-to-and-tools/methods/usability-testing.html')
link3 = Link(title='Emppathy Map', tool_id=3, source='Stanford d school',
             url='https://dschool-old.stanford.edu/wp-content/themes/dschool/method-cards/empathy-map.pdf')
session.add(link1)
session.add(link2)
session.add(link3)
session.commit()

print 'Data has passed!'
