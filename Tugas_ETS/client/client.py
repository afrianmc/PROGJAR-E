import socket
import sys
import os
import time
from threading import Thread
import glob
import json

class Paths:
    def __init__(self):
        self.current_dir = ''

    def get_dir(self):
        return self.current_dir

    def _get_array_dir(self):
        return self.current_dir.split('/')

    def cd(self, dir):
        if dir == '..':
            array_dir = self._get_array_dir()
            self.current_dir = ''

            a_len = len(array_dir)

            for i in range(0, a_len-2):
                print('concat : '+array_dir[i])
                self.current_dir += array_dir[i]
                self.current_dir += '/'

        elif self.current_dir == '':
            self.current_dir = dir + '/'
        else:
            self.current_dir += dir + '/'


class Client(Thread):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = ('127.0.0.1', 6000)
        self.sock.connect(server_addr)
        print('connected '+str(server_addr))
        self.r_path = Paths()
        Thread.__init__(self)

    def dirfunc(self):
        request = {}
        request['command'] = 'dir'
        request['dir'] = self.r_path.get_dir()

        self.sock.sendall(json.dumps(request))
        response = self.sock.recv(1024)
        data = json.loads(response)

        dir_list = data['dir_list']
        print(self.r_path.get_dir())
        for dir in dir_list:
            dir_type = ''
            if dir['is_file']:
                dir_type = 'file'
            else :
                dir_type = 'folder'

            print('-'+dir['name'] + '     [{}]'.format(dir_type))

    def downloadfunc(self, file_name):
        request = {}
        request['command'] = 'download'
        request['path'] = self.r_path.get_dir() + file_name
        self.sock.sendall(json.dumps(request))
        fd = open(file_name, 'wb+', 0)
        response = self.sock.recv(1024)
        data = json.loads(response)
        if data['file_size'] is not None:
            max_size = data['file_size']
            received = 0
            while received < max_size:
                data = self.sock.recv(1024)
                received += len(data)
                fd.write(data)
        fd.close()
        print('Sukses')

    def uploadfunc(self, file_name):
        path = self.r_path.get_dir()+file_name
        fd = open(file_name, 'rb')
        request = {}
        request['command'] = 'upload'
        request['path'] = path
        request['file_size'] = os.path.getsize(file_name)
        self.sock.sendall(json.dumps(request))
        response = self.sock.recv(1024)
        if response == '--OK--':
            for data in fd:
                self.sock.sendall(data)

        print('Sukses')

    def run(self):
        while True:
            commands = raw_input().split(' ')
            command = commands[0]
            if command == 'dir':
                self.dirfunc()
            elif command == 'cd':
                cd_path = commands[1]
                self.r_path.cd(cd_path)
                print(self.r_path.get_dir())
            elif command == 'download':
                self.downloadfunc(commands[1])
            elif command == 'upload':
                self.uploadfunc(commands[1])

if __name__=="__main__":
    Client().start()