import socket
import sys
import threading


def create_server(port, host='localhost'):
    # using 'with' automatically performs socket cleanup
    try:
        with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen()
            print("Started listening on - ", server_socket.getsockname()[0:2])
            while True:
                    client_socket, client_address = server_socket.accept()
                    print("Incoming connection from ", client_address[0:2])
                    response = client_socket.recv(4096)
                    http_response = response.decode("utf-8")
                    http_response_len = len(http_response)
                    print("response type ", type(response))
                    # display the response
                    print("received response of length %d\n" % http_response_len)
                    print(str(response))
                    split_response = http_response.split(' ', 3)
                    command = split_response[0]
                    total_path = split_response[1]
                    path = total_path[1:]  # remove leading /
                    if command.upper() == 'GET':
                        print("serving GET request")
                        try:
                            with open(path, mode='r') as served_file:
                                client_response = "HTTP/1.1 200 OK\n" + \
                                           "Content-Type: text/html\n" + \
                                           "\n"
                                for line in served_file:
                                    client_response += line
                        except OSError:
                            # if file cannot be found
                            client_response = "HTTP/1.1 404 Not Found\n" +\
                                        "\n" +\
                                        "<html><body>404 not found</body></html>\n"
                    client_socket.send(client_response.encode("utf-8"))
                    client_socket.shutdown(socket.SHUT_WR)
                    client_socket.close()
    except KeyboardInterrupt:
        print("\nServer is shutting down")


if not sys.argv[1:]:
    print("No arguments supplied. Using default port of 8080")
    listen_port = 8080
else:
    print("port supplied:", sys.argv[1])
    listen_port = int(sys.argv[1])

server_thread = threading.Thread(target=create_server, args=(listen_port,))
server_thread.start()
