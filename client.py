import socket

class UDPClient:
    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.server_port = 7500  #port to send to the generator server
        self.buffer_size = 1024
        self.message = "" #blank at first
        self.bytes_to_send = "" #blank at first
        self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
   
    def send_message(self, message_In):
        self.message = message_In
        self.bytes_to_send = str.encode(self.message)
        self.udp_socket.sendto(self.bytes_to_send, (self.server_ip, self.server_port))
   
    def set_network_address(self, ip):
        self.server_ip = ip
        self.udp_socket.close()  # Close the existing socket
        self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # Reopen socket