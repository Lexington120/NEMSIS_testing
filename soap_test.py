# Import necessary modules from spyne library
from spyne.application import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.model.complex import Iterable
from spyne.model.primitive import Integer, Unicode

# Define a simple HelloWorld service
class HelloWorldService(ApplicationServiceBase):
    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(ctx, name, times):
        """
        :param name: A string.
        :param times: An integer.
        :return: An iterable of strings.
        """
        for i in range(times):
            yield f"Hello, {name} ({i + 1})"

# Create the WSGI application
application = Application([HelloWorldService],
                          tns='example',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

# Define the WSGI application for your server
wsgi_application = WsgiApplication(application)

# Create a WSGI server (you can use a different WSGI server such as Gunicorn)
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8000, wsgi_application)
    server.serve_forever()
