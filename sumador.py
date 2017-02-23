#! /usr/bin/python3

import socket
"""Operacion suma poniendo en la URL un valor cada vez"""

"""
Simple HTTP Server version 2: reuses the port, so it can be
restarted right after it has been killed. Accepts connects from
the outside world, by binding to the primary interface of the host.

Jesus M. Gonzalez-Barahona and Gregorio Robles
{jgb, grex} @ gsyc.es
TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
"""

# Create a TCP objet socket and bind it to a port
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Let the port be reused if no process is actually using it
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to the address corresponding to the main name of the host
mySocket.bind((socket.gethostname(), 1235))

# Queue a maximum of 5 TCP connection requests

mySocket.listen(5)

# Accept connections, read incoming data, and answer back an HTML page
#  (in an almost-infinite loop; the loop can be stopped with Ctrl+C)

try:
    hay_operando1 = False
    while True:
        print ('Waiting for connections')
        (recvSocket, address) = mySocket.accept()
        print ('Request received:')
        # pasar de bytes a utf-8
        peticion = recvSocket.recv(2048).decode("utf-8", "strict")
        print (peticion)
        recurso = peticion.split()[1][1:]  # lista cortando por espacios
        # aqui voy a tener el valor que me han pasado ya sea una int,float...

        if (recurso == "favicon.ico"):
            recvSocket.send(
                        bytes(
                            "HTTP:/1.1 404 Not found\r\n\r\n" +
                            "<html><body><h1>Not Found</h1></body></html>\r\n",
                            "utf-8"
                        )
            )
            recvSocket.close()
            continue

        if (hay_operando1):
            # todo lo referido al segundo operando
            try:
                valor2 = int(recurso)
                suma = valor1 + valor2
                recvSocket.send(
                            bytes(
                                "HTTP/1.1 200 OK\r\n\r\n" +
                                "<html><body>" +
                                str(valor1) +
                                "+" +
                                str(valor2) +
                                "=" +
                                str(suma) +
                                "</body></html>" +
                                "\r\n",
                                "utf-8"
                            )
                )
                hay_operando1 = False
                recvSocket.close()
            except ValueError:
                print ("No se ha introducido un numero entero")
                recvSocket.send(
                            bytes(
                                "HTTP/1.1 404 Not Found\r\n\r\n" +
                                "<html><body>Error introducir valor"
                                "</body></html>" +
                                "\r\n",
                                "utf-8"
                            )
                )
                recvSocket.close()
        else:
            # todo lo referido al primer operando (todavia no hay operando1)
            try:
                valor1 = int(recurso)
                hay_operando1 = True
                recvSocket.send(
                            bytes(
                                "HTTP/1.1 200 OK\r\n\r\n" +
                                "<html><body>Primer numero introducido:" +
                                str(valor1) +
                                "</body></html>" +
                                "\r\n",
                                "utf-8"
                            )
                )
                recvSocket.close()
            except ValueError:
                print ("No se ha introducido un numero entero")
                recvSocket.send(
                            bytes(
                                "HTTP/1.1 404 Not Found\r\n\r\n" +
                                "<html><body>Error introducir valor"
                                "</body></html>" +
                                "\r\n",
                                "utf-8"
                            )
                )
                recvSocket.close()
                hay_operando1 = False
except KeyboardInterrupt:
    print ("Closing binded socket")
    mySocket.close()
