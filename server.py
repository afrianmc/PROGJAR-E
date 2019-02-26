import select
import socket
import sys
import threading
import random
import times
import Queue

class Server:
    def __init__(self):
        self.host = 'localhost'
        self.port = 5000
        self.size = 1024
        self.backlog = 5
        self.server = None
        self.threads = []

    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.host, self.port))
            self.server.listen(5)

        except socket.error, (value, message):
            if(self.server):
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    def soal(self):
        oper = ['-', '+', '*', '/']
        key = Queue.Queue()

        var1=(random.choice(oper))
        var2=(random.choice(oper))
        var3=(random.choice(oper))
        var4=(random.choice(oper))
        var5=str(random.randrange(1,10))
        var6=str(random.randrange(1,10))
        var7=str(random.randrange(1,10))
        var8=str(random.randrange(1,10))
        var9=str(random.randrange(1,10))
        soal=var9+var1+var8+var2+var7+var3+var6+var4+var5

        hasil = eval(soal)
        key.put(hasil)
        for client in self.threads:
            client.sendsoal(soal)
        time.sleep(10)

    def run(self):
        self.open_socket()
            inputsocket = [self.server]
        running = 1

        while running:
            inputready, outputready, exceptready = select.select(inputsocket, [], [])
            for s in inputready:
                if s == self.server:
                    c = Client(self.server.accept())
                    c.start()
                    self.threads.append(c)

                    conn = threading.activeCount()-1
                    if(conn)<3:
                        for client in self.threads:
                            client.sendsoal('waiting...')
                    elif(conn)==3:
                        for client in self.threads:
                            client.sendsoal('start..')
                        time.sleep(3)
                        self.soal()

                elif sock == sys.stdin:
                    junk = sys.stdin.readline()
                    running = 0

            self.server.close()
            for c in self.threads:
                c.join()

class Client(threading.Thread):
	def __init__(self, (client,address)):
		threading.Thread.__init__(self)
		self.client = client
		self.address = address
		self.size = 1024

        def run(self):
            data=self.client.recv(self.size)

        def sendsoal(self,(mess)):
            if mess:
                self.client.send(mess)
            else:
                self.client.close()
if __name__ == "__main__":
	s = Server()
	s.run()
