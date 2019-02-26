import socket
import sys


server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

try:
	while True:
		data = client_socket.recv(1024)
        sys.stdout.write('jawab: ')
        mess = sys.stdin.readline()
        client_socket.send(mess)

except KeyboardInterrupt:
	client_socket.close()
	sys.exit(0)

