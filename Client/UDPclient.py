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
        