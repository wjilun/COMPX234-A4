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
            elif parts[2]=="CLOSE":
                response = f"FILE {filename} CLOSE_OK"
                data_socket.sendto(response.encode('utf-8'), address)
                print(f"client_adress {client_adress} has closed the file {filename}")
                print("")
                data_socket.close()
                return
    except Exception as e:
        print(f"error when handle file: {e}")
        print("")
        data_socket.close()
        return        

def handle_download(data,client_address,server_socket):
    try:
        request = data.decode('utf-8')
        parts=request.split()
        filename=parts[1]
        if not os.path.exists(filename):
            error_response = f"ERR {filename} NOT_FOUND"
            server_socket.sendto(error_response.encode('utf-8'), client_address)
            return
        with open(filename, 'rb') as f:
            file_size = len(f.read())
        data_port = random.randint(50000, 51000)
        file_md5=hashlib.md5()
        with open(filename, 'rb') as f:
            while content := f.read(4096):
                file_md5.update(content)
        response = f"OK {filename} SIZE {file_size} PORT {data_port} MD5 {file_md5.hexdigest()}"
        server_socket.sendto(response.encode('utf-8'), client_address)
        print(f"client_address {client_address} ,file {filename} size {file_size} byte, data_port {data_port}, MD5{file_md5.hexdigest()}")
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data_socket.bind(('localhost', data_port))
        print(f"sever has connect to {data_port}, handle {client_address} request")
