import socket
import threading

class UDPServer:
    def __init__(self, ip_In): 
        self.ip = ip_In 
        self.port = 7501  
        self.buffer_size = 1024
        self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
        self.running = False  # Track server status
        self.received_data = [] #list for storing data from traffic generator

        self.red_team_eids = set()
        self.green_team_eids = set()
        
        self.bind_server()  

    def bind_server(self):
        try:
            self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow rebinding
            self.udp_socket.bind((self.ip, self.port))
            print(f"UDP socket created on {self.ip}:{self.port}") 
        except Exception as e:
            print(f"{e}")

        
    def set_network_address(self, ip_In):
        #Stops the current server and restarts it with a new IP address.
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

    
    #2 functions for helping points updating
    def update_team_info(self, red_team_players, green_team_players):
        self.red_team_eids.clear()
        self.green_team_eids.clear()
        
        # Add all equipment IDs from the red team
        for player in red_team_players:
            if player.equipment_id:
                self.red_team_eids.add(player.equipment_id)
                
        # Add all equipment IDs from the green team
        for player in green_team_players:
            if player.equipment_id:
                self.green_team_eids.add(player.equipment_id)

    def friendly_fire(self, s_eid, t_eid):
        if s_eid in self.red_team_eids and t_eid in self.red_team_eids:
            return True
        if s_eid in self.green_team_eids and t_eid in self.green_team_eids:
            return True
        return False


    '''
    Player A sends "A_id:B_id" to server on port 7501>
    Parses shooter and target indentity> Record hit in recieved_data> Send ACK
    Update points, display, game_events
    '''
    def run_server(self): #runs the loop to keep the server listening 
        print(f"UDP server up and listening on {self.ip}:{self.port}")  
        while self.running:
            try:
                bytes_address_pair = self.udp_socket.recvfrom(self.buffer_size)  
                message = bytes_address_pair[0]
                address = bytes_address_pair[1]

                message_str = message.decode()
                print(f"Message from Client: {message_str}")
                print(f"Client IP Address: {address}")
                #message format should be integer:integer
                # eid of player transmitting : eid of player hit 
                try:
                    sender_eid, target_eid = map(int, message_str.strip().split(":"))
                    self.received_data.append((sender_eid, target_eid))

                    #acknowledge hit registration
                    # MOVED TO GAME AND CLIENT AS THIS IS ILLEGAL!!!
                    # response_address = (address[0], 7500)
                    # self.udp_socket.sendto(str(target_eid).encode(), response_address)
                    # print(f"Sent response: {target_eid} to {response_address}")
                except Exception as e:
                    print(f"Error Processing: {e}")
            except Exception as e:
                print(f"Server socket closed. {e}")
                break  

    def stop(self): #stops the server running and closes the socket
        if self.running:
            self.running = False
            self.udp_socket.close()
            self.udp_socket = None
            print("UDP server has been stopped")

    def get_data(self):
        #Returns the list of(sender_eid, eid_of_player_hit) tuples
        return self.received_data 

    def clear_data(self):
        self.received_data = []
