import socket
import threading

bind_ip = '0.0.0.0'
bind_port = 8889

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

print('Listening on {}:{}'.format(bind_ip, bind_port))


def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 10)
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 50)
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 6)
    while request != "-1":

        print('Received {}'.format(request))
        client_socket.send(b'ACK!')
        request = client_socket.recv(1024)

    client_socket.close()


while True:
    client_sock, address = server.accept()
    client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    client_handler = threading.Thread(
        target=handle_client_connection,
        # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
        args=(client_sock,)
    )
    client_handler.start()
