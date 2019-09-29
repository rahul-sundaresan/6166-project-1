import socket
import sys
import threading

server_hostname, server_port, http_command, http_file_path = sys.argv[1:]
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((server_hostname, int(server_port)))
    if http_command.upper() == "GET":
        # send some data
        request = "GET " + http_file_path + " HTTP/1.1\r\nHost:%s\r\n\r\n" % server_hostname
        client_socket.send(request.encode())
        response = client_socket.recv(4096)
        http_response = repr(response)
        http_response_len = len(http_response)

        # display the response
        print("received response of length %d\n" % http_response_len)
        print(str(response))

    elif http_command.upper() == "PUT":
        request = "PUT / HTTP/1.1\r\nHost:%s\r\n\r\n" % server_hostname
