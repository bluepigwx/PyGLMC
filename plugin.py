import socket


_host = "localhost"
_port = 9987

class Plugin:
    def __init__(self):
        self.socket = None
        
    
    def connect(self):
        if self.socket != None:
            raise Exception("socket not none")
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(_host, _port)
        except Exception as e:
            pass