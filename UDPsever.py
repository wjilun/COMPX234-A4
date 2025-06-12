import socket
import threading
import random
import base64
import os
import hashlib

def handle_file(data_socket,filename,client_adress):
    try:
        while True:
            data,address=data_socket.recvfrom(1024)
            request = data.decode('utf-8')
            parts = request.split()
            if parts[2]=="GET":
                s=int(parts[4])
                e=int(parts[6])
                try:
                    with open(filename, 'rb') as f:
                        f.seek(s)
                        content= f.read(e - s + 1)
                    encoded_cont = base64.b64encode(content).decode('utf-8')
                    response = f"FILE {filename} OK START {s} END {e} DATA {encoded_cont}"
                    data_socket.sendto(response.encode('utf-8'), address)
                except Exception as e:
                    print(f"error when get data information: {e}")
            




    