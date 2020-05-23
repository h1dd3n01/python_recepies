'''
    You want to create a server that talks with clients by TCP protocol.
    We will create a filelike interface on socket
    That can be achieved with socketserver.
'''

from socketserver import StreamRequestHandler, TCPServer


class EchoHandler(StreamRequestHandler):
    def __init__(self):
        print('Got connection from {}'.format(self.client_address))
        for line in self.rfile:
            # self.wfile is a filelike object for writing
            self.wfile.write(line)


if __name__ == '__main__':
    serv = TCPServer(('', 20000), EchoHandler)
    serv.serve_forever()

    '''
        Here you create a special class that realisez the method handle() for
        handling client connections. Attribute requests is a client socket,
        client_address contains the client ip.
        Socketserver make the connection quite simple for TCP like servers.
        Bare in mind tho, that this connection is synchronous.
        In order to support async connections fork from ForkingTCPServer or
        ThreadingTCPServer.
            
            # Example
            from socketserver import ThreadingTCPServer
            
            
            if __name__ == '__main__':
                serv = ThreadingTCPServer(('', 20000), EchoHandler)
                serv.serve_forever()
                
        Problem with the example above is, it creates a new process for each
        connection.
        Due to no limits on number of allowed connections, some hacker can 
        create unlimited number of processes that will brake your system.
        
        
        if __name__ == '__main__':
            from threading import Thread
            NWORKERS = 16
            serv = TCPServer(('', 20000), EchoHandler)
            for n in range(NWORKERS):
                t = Thread(target=serv.server_forever)
                t.daemon = True
                t.start()
            serv.serve_forever()
            
        Usually a TCPServer binds a socket and connects it during connection.
        Tho sometimes you would want to configure a socket by giving it params.
        In order to do that give the socket the following argument bind_and_activate=False .
        
        
        if __name__ == '__main__':
            serv = TCPServer(('', 20000), EchoHandler, bind_and_activate=False)
            # Set socket parameters
            serv.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            # Bind and activate
            serv.serv_bind()
            serv.server_activate()
            serv.serve_forever()
            
        Example above is very commonly user. It allows the server to bind the socket to
        previously used port
        
        StreamRequestHandler is more flexible and supports more opportunities, that can
        be included in additional parameters of a class. Example.
        
        
        class EchoHandler(StreamRequestHandler):
            timeout = 5 # Timeout for all socket operations
            rbufsize = -1 # Size of Buffers reading
            wbufsize = 0 # Size of buffers writing
            disable_nagle_algorithm = False # sets option TCP_NODELAY
            
            def handle(self):
                print('Got connection from {}'.format(self.client_address)
                try:
                    for line in self.rfile:
                        $ self.wfile - filelike object for reading
                        self.write.write(line)
                except socket.timeout:
                    print('Time out!') 
    '''

    '''
        You have a CIDR-address of type 123.45.67.64/27. and you want to
        generate the range of all ip addresses, that are available within the netmask
        
        
        >>> import ipaddress
        >>> net = ipaddress.ip_network('123.45.67.64/27')
        >>> net
        IPv4Network('123.45.67.64/27')
        >>> for a in net:
            print(a)
        123.45.67.64
        123.45.67.65
        123.45.67.66
        123.45.67.67
        123.45.67.68
        ...
        123.45.67.95
        >>> net6 = ipaddress.ip_network('12:3456:78:90ab:cd:ef01:23:30/125')
        >>> net6
        IPv6Network('12:3456:78:90ab:cd:ef01:23:30/125')
        >>> for a in net6:
        ...
        print(a)
        12:3456:78:90ab:cd:ef01:23:30
        12:3456:78:90ab:cd:ef01:23:31
        12:3456:78:90ab:cd:ef01:23:32
        12:3456:78:90ab:cd:ef01:23:33
        12:3456:78:90ab:cd:ef01:23:34
        12:3456:78:90ab:cd:ef01:23:35
        12:3456:78:90ab:cd:ef01:23:36
        12:3456:78:90ab:cd:ef01:23:37
        >>>
    '''

    '''
       You want to have the ability to control or talk to your program through a remote connection
       , through the network using REST-interface. But you don't want to install a complete web-framework.    
        One of the most simplest ways to build up a REST-interface is through small library
        that is based on WSGI standarts .
        
    '''

import cgi


def notfound_404(environ, start_response):
    start_response('404 not found', [('Content-type', 'text/plain')])
    return [b'Not Found']


class PathDispatcher:
    def __init__(self):
        self.pathmap = {}

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        params = cgi.FieldStorage(environ['wsgi.input'],
                                  environ=environ)
        method = environ['REQUEST_METHOD'].lower()
        environ['params'] = {key: params.getvalue(key) for key in params}
        handler = self.pathmap.get((method, path), notfound_404)
        return handler(environ, start_response)

    def register(self, method, path, function):
        self.pathmap[method.lower(), path] = function
        return function

    '''
        In order to use this Dispatcher you simply need to write
        
        import time
        _hello_resp = 
        <html>
            <head>
                <title>Hello {name}</title>
            </head>
            <body>
                <h1>Hello {name}!</h1>
            </body>
        </html>
        def hello_world(environ, start_response):
            start_response('200 OK', [ ('Content-type','text/html')])
            params = environ['params']
            resp = _hello_resp.format(name=params.get('name'))
            yield resp.encode('utf-8')
            
            
        _localtime_resp = 
        <?xml version="1.0"?>
        <time>
        <year>{t.tm_year}</year>
        <month>{t.tm_mon}</month>
        <day>{t.tm_mday}</day>
        <hour>{t.tm_hour}</hour>
        <minute>{t.tm_min}</minute>
        <second>{t.tm_sec}</second>
        </time>
        
        def localtime(environ, start_response):
            start_response('200 OK', [ ('Content-type', 'application/xml') ])
            resp = _localtime_resp.format(t=time.localtime())
            yield resp.encode('utf-8')
            
            
        if __name__ == '__main__':
            from resty import PathDispatcher
            from wsgiref.simple_server import make_server
            # Create dispatcher and register a function
            dispatcher = PathDispatcher()
            dispatcher.register('GET', '/hello', hello_world)
            dispatcher.register('GET', '/localtime', localtime)
            # Run basic server
            httpd = make_server('', 8080, dispatcher)
            print('Serving on port 8080...')
            httpd.serve_forever()
    '''

    '''
        You run many Python interpreters possibly on many computers.
        You want to exchange data with interpreters through messaging.
        
        Through the help of a module multiprocessing.connection it is very easy
        to make a connection between interpreters. Here is a example:
        
    '''


from multiprocessing.connection import Listener


def echo_client(conn):
    try:
        while True:
            msg = conn.recv()
            conn.send(msg)
    except EOFError:
        print('Connection closed')


def echo_server(address, authkey):
    serv = Listener(address, authkey=authkey)
    while True:
        try:
            client = serv.accept()
            echo_client(client)
        except Exception as e:
            print(e.args)


echo_server(('', 25000), authkey=b'peekaboo')

'''
    Here is a simple example of connecting to the server and sending
    a message
    
    >>> from multiprocessing.connection import Client
    >>> c = Client(('localhost', 25000), authkey=b'peekaboo')
    >>> c.send('hello')
    >>> c.recv()
    'hello'
    >>> c.send(42)
    >>> c.recv()
    42
    >>> c.send([1, 2, 3, 4, 5])
    >>> c.recv()
    [1, 2, 3, 4, 5]
'''

'''
    ------------------- Google -> RPC ----------------------------
'''

'''
    You want to realize a simple client authentication that connect to
    servers, but you don't need complex solutions like SSL.
    
    Simple but yet effective way to authenticate can be realised through
    a handshake connection using module hmac. Here's an example:
    
'''

import hmac
import os


def client_authentication(connetion, secret_key):
    msg = connetion.recv(32)
    hash = hmac.new(secret_key, msg)
    digest = hash.digest()
    connetion.send(digest)


def server_authentication(connection, secret_key):
    msg = os.urandom(32)
    hash = hmac.new(secret_key, msg)
    digest = hash.digest()
    response = connection.recv(len(digest))
    return hmac.compare_digest(digest, response)


'''
    The main idea is, before creating a connection server gives the client
    a message of random bytes(In this case they are generated with os.random).
    And the client and the server decrypt the hash of random data using hma and secret_key
    That is known only to both sides.
    The comparison of digests should be used with the fiunction hmac.compare_digest().
    It is written to limit timing attacks and should be used instead of a standart 
    operation ==.
    Чтобы использовать эти функции, вы должны включить их в существующий се-
    тевой код или код системы обмена сообщениями. Например, серверный код с со-
    кетами может выглядеть как-то так:
    
    from socket import socket, AF_INET, SOCK_STREAM
    secret_key = b'peekaboo'
    def echo_handler(client_sock):
        if not server_authenticate(client_sock, secret_key):
        client_sock.close()
        return
        while True:
            msg = client_sock.recv(8192)
            if not msg:
                break
        client_sock.sendall(msg)
        
    def echo_server(address):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(address)
        s.listen(5)
        while True:
            c,a = s.accept()
            echo_handler(c)
echo_server(('', 18000))


    В клиенте нужен примерно такой код:
    
    from socket import socket, AF_INET, SOCK_STREAM
    
    secret_key = b'peekaboo'
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('localhost', 18000))
    client_authenticate(s, secret_key)
    s.send(b'Hello World'
'''

'''
    You want to realize a network service, using sockets, where clients and 
    authenticate each other and encrypt data trough SSL.
    Module ssl give the ability for adding SSL to low level connections
    based on ssl. Particulary function ssl.wrap_socket() takes in already existing
    socket and wraps it with SSL layer. Here is a example of a simple
    EchoServer.
'''

from socket import socket, AF_INET, SOCK_STREAM
import ssl

KEYFILE = 'server_key.pem'  # Passable key to the server
CERTFILE = 'server_cert.pem'  # Server certificate (passable to client)


def echo_client(s):
    while True:
        data = s.recv(8192)
        if data == b'':
            break
        s.send(data)
    s.close()
    print('Connection closed')


def echo_server(address):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(1)

    # Wraps with ssl layer, requires client sertification
    s_ssl = ssl.wrap_socket(s,
                            keyfile=KEYFILE,
                            certfile=CERTFILE,
                            server_side=True)

    # Waits for connection
    while True:
        try:
            c, a = s_ssl.accept()
            print('Got connection', c, a)
            echo_client(c)
        except Exception as e:
            print('{}: {}'.format(e.__class__.__name__, e))


echo_server(('', 20000))

'''
        Here is a interactive session, that shows how client connects to server.
        Client asks a server its sertificate and checks it.
        
        >>> from socket import socket, AF_INET, SOCK_STREAM
        >>> import ssl
        >>> s = socket(AF_INET, SOCK_STREAM)
        >>> s_ssl = ssl.wrap_socket(s,
        ...
        cert_reqs=ssl.CERT_REQUIRED,
        ...
        ca_certs = 'server_cert.pem')
        >>> s_ssl.connect(('localhost', 20000))
        >>> s_ssl.send(b'Hello World?')
        12
        >>> s_ssl.recv(8192)
        b'Hello World?'
        >>>
        
        
    Problem with this low level sockets hacking is, it doesn't work well with existing network
    services already realised in the standart library. For example, big part of server code
    (HTTP, XML-RPC, and so on) is based on socketserver library. Client code also realizes on
    more higher level abstraction. In already existing services we can add SSL, but for that
    we need a different approach.
    First of all, we can add SSL into server as classMixin
'''

import ssl


class SSLMixin:
    def __init__(self, *args, keyfile=None, cerfile=None,
                 ca_certs=None, cert_reqs=ssl.NONE, **kwargs):
        self._keyfile = keyfile
        self._certfile = cerfile
        self._ca_certs = ca_certs
        self._cert_reqs = cert_reqs
        super().__init__(*args, **kwargs)

    def get_request(self):
        client, addr = super().get_request()
        client_ssl = ssl.wrap_socket(client, keyfile=self._keyfile,
                                     certfile=self._certfile,
                                     ca_certs=self._ca_certs,
                                     cert_reqs=self._cert_reqs,
                                     server_side=True)

        return client_ssl, addr
