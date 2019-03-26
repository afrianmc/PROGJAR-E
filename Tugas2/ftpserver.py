import socket                   

port = 60000                    
s = socket.socket()             
host = socket.gethostname()     
s.bind((host, port))            
s.listen(5)                     

print 'Server listening....'

while True:
	conn, addr = s.accept() 
	print 'Got connection from', addr
	filename = conn.recv(1024)
	print "Client requesting => "+filename
	f = open(filename,'rb')
	l = f.read(1024)
	while (l):
		conn.send(l)
		print('Sending data....')
		l = f.read(1024)
	f.close()

	print('Done sending')
	conn.close()

