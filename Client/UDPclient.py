import socket
import base64
import hashlib

class UDPclient:
    def __init__(self, server_host, server_port):
       self.server_address = (server_host, server_port)
       self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       self.client_socket.settimeout(1.0)

    def calculate_md5(self, filename):
        hash_md5 = hashlib.md5()
        try:
            with open(filename, 'rb') as f:
                for content in iter(lambda: f.read(4096), b""):
                    hash_md5.update(content)
        except Exception as e:
            print(f"error when calculate: {e}")
            return None
        return hash_md5.hexdigest()

    def send_request_with_retry(self, message, target_address=None, max_retries=5):
        if target_address is None:
            target_address = self.server_address
        initial_timeout = 1.0
        for retry in range(max_retries):
            try:
                self.client_socket.sendto(message.encode('utf-8'), target_address)
                timeout = initial_timeout * (2 ** retry)
                self.client_socket.settimeout(timeout)
                response, _ = self.client_socket.recvfrom(4096)
                return response.decode('utf-8')
            except socket.timeout:
                print(f"time out {retry+1}/{max_retries},beyond time: {timeout} second")
            except Exception as e:
                print(f"error when send request: {e}")
        return None
    
    def download_file(self, filename):
        download_request = f"DOWNLOAD {filename}"
        response = self.send_request_with_retry(download_request)
        if not response or not response.startswith("OK"):
            print(f"fail to download")
            return False     
        parts = response.split()
        file_size = int(parts[3])
        data_port = int(parts[5])
        server_md5 = parts[7]
        print(f"file {filename} size: {file_size} byte, data_port: {data_port}")
        data_address = (self.server_address[0], data_port)
        block_size = 1000
        received_data = bytearray(file_size)
        for start in range(0, file_size, block_size):
            end = min(start + block_size - 1, file_size - 1)
            block_request = f"FILE {filename} GET START {start} END {end}"
            response = self.send_request_with_retry(block_request, target_address=data_address)
            if not response or not response.startswith(f"FILE {filename} OK"):
                print(f"get block {start}-{end} failed,respose: {response if response else 'no response'}")
                close_request = f"FILE {filename} CLOSE"
                self.send_request_with_retry(close_request, data_address)
            try:
                parts= response.split("DATA ", 1)
                data_part=parts[1]
                decoded_data = base64.b64decode(data_part)
                if start <= end and len(decoded_data) == (end - start + 1):
                    received_data[start:start+len(decoded_data)] = decoded_data
                    progress = (start / file_size) * 100
                    print(f"Accept {start}-{end},progress: {progress:.1f}%")
                else:
                    print(f"block {start}-{end} Duplication or loss, retransmission")
            except Exception as e:
                print(f" error parsing the response: {e}")
                close_request = f"FILE {filename} CLOSE"
                self.send_request_with_retry(close_request, data_address)   
            

