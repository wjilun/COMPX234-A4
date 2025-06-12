import socket
import threading
import random
import base64
import os
import hashlib

def handle_data_request(data_socket,filename,client_adress)