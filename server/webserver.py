from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import cgi
from render_template import render_template
from models.dbconfig import Restaurant


class WebServer(BaseHTTPRequestHandler):
    """  Webserver Handler """
    def do_GET(self):
        """ Handle all GET request """
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = render_template('../templates/restaurant/index.html')
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                output = render_template('../templates/restaurant/new.html')
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                output = render_template("../templates/restaurant/edit.html")
                self.wfile.write(output)
                return

        except IOError:
            self.send_response(404, "File Not Found %s" % self.path)

    def do_POST(self):
        """ handle all post request """
        try:
            if self.path.endswith("/restaurant/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurantArray = fields.get('restaurant')

                    # create a new Restaurant
                    newRestaurantObject = Restaurant()
                    newRestaurantObject.save(restaurantArray[0])

                    self.send_response(301)
                    self.send_header('Content-Type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    return
        except:
            pass


def main():
    """ Manage the server """
    try:
        PORT = 8080
        server = HTTPServer(('', PORT), WebServer)
        print "Web server running on port %s" % PORT
        server.serve_forever()
    except KeyboardInterrupt:
        print "ctrl-c entered, stopping web server ...."
        server.socket.close()


if __name__ == "__main__":
    main()
