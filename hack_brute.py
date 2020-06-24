import socket
import sys
import string
import itertools

args = sys.argv
if len(args) == 3:
    hostname, port = args[1], int(args[2])

charset = string.ascii_lowercase + string.digits

with socket.socket() as client_socket:
    address = (hostname, port)
    client_socket.connect(address)
    previous = [""]
    current = []
    iterator = itertools.product(charset, previous)
    password = None
    response = None

    while response != "Connection success!":
        try:
            message = "".join(next(iterator))
            current.append(message)
            message = message.encode()
            client_socket.send(message)
            response = client_socket.recv(1024)
            response = response.decode()
            if response == "Connection success!":
                password = message.decode()
                break
            elif response == "Wrong password!":
                continue
            else:
                break
        except StopIteration:
            previous = current
            current = []
            iterator = itertools.product(charset, previous)

    print(password)


