import random
import UDPclient
import socket

class UDPclientWithLoss(UDPclient.UDPclient):
    def __init__(self, server_host, server_port, packet_loss_rate=0.2):
        self.server_address = (server_host, server_port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(1.0)
        self.packet_loss_rate = packet_loss_rate