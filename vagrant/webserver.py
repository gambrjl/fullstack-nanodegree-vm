from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

#Create and Connect to database
engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Make a new Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder='New Restaurant Name' >"
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"

                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                restaurantID = self.path.split("/")[2]
                restaurantQuery = session.query(Restaurant).filter_by(id = restaurantID).one()
                if restaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = "<html><body>"
                    output += "<h1>"
                    output += restaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantID
                    output += "<input name='newRestaurantName' type='text' placeholder='%s'>" % restaurantQuery.name
                    output += "<input type='submit' value='Rename'>"
                    output += "</form>"

                    self.wfile.write(output)

            if self.path.endswith("/delete"):
                restaurantID = self.path.split("/")[2]
                restaurantQuery = session.query(Restaurant).filter_by(id = restaurantID).one()
                if restaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = "<html><body>"
                    output += "<h1>"
                    output += "Are you sure you want to delete %s" % restaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurantID
                    output += "<input type='submit' value='Delete'>"
                    output += "</form>"

                    self.wfile.write(output)

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output=""
                output += "<html><body>"
                
                output += "<a href='/restaurants/new'> Make a New Restaurant Here </a>"

                items = session.query(Restaurant).all()
                for item in items:
                    output += "<p>"
                    output += item.name
                    output += "<br />"
                    output += "<a href='/restaurants/%s/edit'>Edit</a>" % item.id
                    output += "<br />"
                    output += "<a href='/restaurants/%s/delete'>Delete</a>" % item.id
                    output += "</p>"

                output += "</body></html>"
                self.wfile.write(output)
                print output 
                return

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output=""
                output += "<html><body>"
                output += "Hello"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like to say?</h2><input name='message' type='text><input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output=""
                output += "<html><body>&#161Hola! <a href = '/hello'>Back to Hello</a>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like to say?</h2><input name='message' type='text><input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return
        except IOError:
            self.send_error(404, "File not found %s" % self.path)
    
    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                #messagecontent = fields.get('newRestaurantName')
                restaurantID = self.path.split("/")[2]

                query = session.query(Restaurant).filter_by(id = restaurantID).one()
                if query != []:
                    #query.name = messagecontent[0]
                    session.delete(query)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')
                restaurantID = self.path.split("/")[2]

                query = session.query(Restaurant).filter_by(id = restaurantID).one()
                if query != []:
                    query.name = messagecontent[0]
                    session.add(query)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()

if __name__ == '__main__':
    main()