import socket

class UDPServer:
    def __init__(self, ip_In): #unless changed will be 127.0.0.1
        self.ip = ip_In
        self.port = 7501 #port that that receives from generator client
        self.buffer_size = 1024
        self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) #creates socket
        self.bind_server() #binds the server
   
    def bind_server(self):
        self.udp_socket.bind((self.ip, self.port))
        print(f"UDP server up and listening on {self.ip}:{self.port}") #server successfully running
   
    def set_network_address(self, ip_In): #method for changing the network address
        self.ip = ip_In #set the ip
        self.udp_socket.close() #close the default socket
        self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) #creates new socket and binds it
        self.bind_server()
   
    def start(self): #this is only called once the network address has been determined
        while True:
            bytes_address_pair = self.udp_socket.recvfrom(self.buffer_size) #listen to the generator client
            message = bytes_address_pair[0]
            address = bytes_address_pair[1]
           
            client_msg = f"Message from Client: {message.decode()}" #receive generator client message
            client_ip = f"Client IP Address: {address}"
           
            print(client_msg)
            print(client_ip)
           
            self.udp_socket.sendto(self.bytes_to_send, address)
   
    def sendGameInfo(self): #implement this later, this wil be used to send the info
        #from generator client to update our game screen
        pass