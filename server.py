import socket
import threading

class UDPServer:
    def __init__(self, ip_In): 
        self.ip = ip_In 
        self.port = 7501  
        self.buffer_size = 1024
        self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
        self.running = False  # Track server status
        self.bind_server()  

    def bind_server(self):
        try:
            self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow rebinding
            self.udp_socket.bind((self.ip, self.port))
            print(f"UDP socket created on {self.ip}:{self.port}") 
        except Exception as e:
            print(f"Error binding server: {e}")  # Add logging

        
    def set_network_address(self, ip_In):
        """Stops the current server and restarts it with a new IP address."""
        self.stop()  
        self.ip = ip_In  
        self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  
        self.bind_server()
        self.start() #automatically start in new thread when network address changes

    def start(self): #starts server in the background on a thread so it doesn't interfere with main game loop
        if not self.running:
            self.running = True
            server_thread = threading.Thread(target=self.run_server, daemon=True)
            server_thread.start()
    
    def run_server(self): #runs the loop to keep the server listening 
        print(f"UDP server up and listening on {self.ip}:{self.port}")  
        while self.running:
            try:
                bytes_address_pair = self.udp_socket.recvfrom(self.buffer_size)  
                message = bytes_address_pair[0]
                address = bytes_address_pair[1]

                print(f"Message from Client: {message.decode()}")
                print(f"Client IP Address: {address}")

            except Exception as e:
                print(f"Server socket closed. {e}")
                break  

    def stop(self): #stops the server running and closes the socket
        if self.running:
            self.running = False
            self.udp_socket.close()
            print("UDP server has been stopped")
