import random
import UDPclient
import socket

class UDPclientWithLoss(UDPclient.UDPclient):
    def __init__(self, server_host, server_port, packet_loss_rate=0.2):
        self.server_address = (server_host, server_port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(1.0)
        self.packet_loss_rate = packet_loss_rate

    def send_request_with_retry(self, message, target_address=None, max_retries=5):
        if target_address is None:
            target_address = self.server_address
        initial_timeout = 1.0
        for retry in range(max_retries):
            try:
                if random.random() >= self.packet_loss_rate:
                    self.client_socket.sendto(message.encode('utf-8'), target_address)
                else:
                    print(f"loss: {message[:10]}...")
                    continue
                timeout = initial_timeout * (2 ** retry)
                self.client_socket.settimeout(timeout)
                if random.random() < self.packet_loss_rate:
                    print("loss(accept)")
                    raise socket.timeout()    
                response, _ = self.client_socket.recvfrom(4096)
                return response.decode('utf-8')
            except socket.timeout:
                print(f"time out {retry+1}/{max_retries},beyond time: {timeout} 秒")
            except Exception as e:
                print(f"error when send: {e}")
        return None    