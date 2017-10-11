from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi



# import CRUD Operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# https://docs.python.org/2/library/basehttpserver.html
class WebServerHandler(BaseHTTPRequestHandler):


    def do_GET(self):
        try:
            # Create new
            if self.path.endswith('/restaurants/new'):
                send_header200(self)
                output = '<html><body><h1>Make a New Restaurant</h1>'
                # The enctype attribute specifies how the form-data should be encoded
                output = '''<form method='POST' enctype='multipart/form-data'
                             action='/restaurants/new'>
                               <input name='newRestaurantName' type='text'
                                placeholder='New Restaurant Name'>
                               <input type='submit' value='Create'>
                             </form></body></html>'''
                self.wfile.write(output)
                return
            # Edit
            if self.path.endswith("/edit"):
                restaurantIDPath, myRestaurantQuery = filter_restaurant(self)
                if myRestaurantQuery:
                    send_header200(self)
                    output = '<html><body><h1>'+myRestaurantQuery.name+'</h1>'
                    output += '''<form method='POST' enctype='multipart/form-data' 
                                 action='/restaurants/%s/edit' >''' % restaurantIDPath
                    output += '''<input name='newRestaurantName' type='text'
                                 placeholder='%s'>''' % myRestaurantQuery.name
                    output += '''<input type = 'submit' value = 'Rename'>
                                 </form></body></html>'''
                    self.wfile.write(output)
            # Delete
            if self.path.endswith("/delete"):
                restaurantIDPath, myRestaurantQuery = filter_restaurant(self)
                if myRestaurantQuery:
                    send_header200(self)
                    output = '<html><body>'
                    output += "<h1>Are you sure you want to delete %s?" % myRestaurantQuery.name
                    output += '''<form method='POST' enctype='multipart/form-data' 
                                 action='/restaurants/%s/delete'>''' % restaurantIDPath 
                    output += '''<input type = 'submit' value = 'Delete'>
                                 </form></body></html>'''
                    self.wfile.write(output)

            if self.path.endswith('/restaurants'):
                restaurants = session.query(Restaurant).all()
                send_header200(self)
                output = '<html><body>'
                for restaurant in restaurants:
                    output += restaurant.name
                    output += '''</br><a href='/restaurants/%s/edit'>Edit</a>
                                 </br><a href ='/restaurants/%s/delete'>Delete</a>
                                 </br></br></br>''' % (restaurant.id, restaurant.id)
                output += '</body></html>'
                self.wfile.write(output)
                return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            # edit
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    # get id
                    restaurantIDPath, myRestaurantQuery = filter_restaurant(self)
                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        go_restaurants(self)
            # new
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    # create new Restaurant object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()
                    go_restaurants(self)

            # delete
            if self.path.endswith("/delete"):
                restaurantIDPath, myRestaurantQuery = filter_restaurant(self)
                if myRestaurantQuery:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    go_restaurants(self)

        except:
            pass



def main():
    try:
        port = 8080
        # host is empty HTTPServer(('[host],[port]))
        server = HTTPServer(('', port), WebServerHandler)
        print 'Web Server running on port {}'.format(port)
        server.serve_forever()
    # trigger when the user pressed ^C
    except KeyboardInterrupt:
        print '^C entered, stopping the web server...'
        server.socket.close()


def send_header200(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()


def go_restaurants(self):
    self.send_response(301)
    self.send_header('Content-type', 'text/html')
    self.send_header('Location', '/restaurants')
    self.end_headers()


def filter_restaurant(self):
    restaurantIDPath = self.path.split("/")[2]
    query = session.query(Restaurant).filter_by(
        id=restaurantIDPath).one()
    return restaurantIDPath, query 
# execute
if __name__ == '__main__':
    main()

