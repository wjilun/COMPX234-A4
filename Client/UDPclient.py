import socket
import base64
import hashlib

def __init__(self, server_host, server_port):
    self.server_address = (server_host, server_port)
    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.client_socket.settimeout(1.0)