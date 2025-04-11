import pygame
from photon_db import PDB
from client import UDPClient
from server import UDPServer
from player import Player
import ipaddress
import render

FONT = None
TITLE_FONT = None
BUTTON_FONT = None
app_client = None
app_server = None


'''
During startup intialize:
UDP Client (port 7500) - Broadcasts to connected equipment
UDP Server (port 7501) - Recieves messages from individual equipment
both at network (127.0.0.1), default
'''

def init_game():
    global FONT, TITLE_FONT, BUTTON_FONT, app_client, app_server
    FONT = pygame.font.SysFont('Arial', 20)
    TITLE_FONT = pygame.font.SysFont('Arial', 24, bold=True)
    BUTTON_FONT = pygame.font.SysFont('Arial', 14)

    render.font_init(FONT, TITLE_FONT, BUTTON_FONT)

    # initialize pygame mixer for music
    pygame.mixer.init()

    app_client = UDPClient("127.0.0.1") #default 
    app_server = UDPServer("127.0.0.1") #default
    app_server.start()

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip) #tries to create an IP object like "192.168.1.1"
        return True
    except ValueError:
        return False

class GameState:
    def __init__(self):
        self.red_team = [Player() for _ in range(15)]
        self.green_team = [Player() for _ in range(15)]
        self.current_team = "red"  
        self.current_index = 0
        self.active_input = "p_id"
        self.previous_input = None
        self.input_text = ""
        self.current_player_id = None
        self.db_connection = None
        self.db = PDB()
        self.connect_to_db()
        self.active_view = "entry"

        self.running = False
        self.gameOver = False
        self.game_events = []
        self.timer = 6*60*60
        self.counting = False
        self.countDown = 30
        #Track index of last processed data point
        self.last_processed_i = 0
         # Music tracks and management
        self.available_tracks = ["Track01.mp3", "Track02.mp3", "Track03.mp3", 
                            "Track04.mp3", "Track05.mp3", "Track06.mp3", 
                            "Track07.mp3", "Track08.mp3"]
        self.current_track = None
        self.played_tracks = []

        for team in [self.red_team, self.green_team]:
            for player in team:
                player.score = 0

    def connect_to_db(self):
        if not self.db.connect():
            print("Failed to connect to database")

    def query_codename(self, player_id):
        if not player_id.strip().isdigit():
            return 
        
        player = self.db.get_player(int(player_id))
        return player['codename'] if player else None

    def add_new_player(self, player_id, codename):
        """Inserts a new player into the database."""
        if not player_id.strip().isdigit() or not codename.strip():
            return False

        player = self.db.get_player(int(player_id))
        if player:
            return True
        else:
            return self.db.add_player(int(player_id), codename)
    
    def update_codename(self, player_id, newName):
        if not player_id or not str(player_id).strip().isdigit() or not newName or not newName.strip():
            print(f"Invalid player ID/codename: {player_id}, {newName}")
            return False
        
        if hasattr(self.db, 'update_player') and callable(getattr(self.db, 'update_player')):
            return self.db.update_player(int(player_id), newName.strip())
        else:
            return self.db.add_player(int(player_id), newName.strip())

    def assign_equipment(self, player_id, equipment_id):
        if not player_id.strip().isdigit() or not equipment_id.strip().isdigit():
            return False
        return self.db.set_EquipID(int(player_id), int(equipment_id))
    
    def override_player(self, player_id):
        if player_id and str(player_id).isdigit():
            try:
                self.db.remove_EquipID(player_id)
                return True
            except:
                print(f"⚠️ Failed to remove equipment of {player_id}")
                return False
        return False

    def play_random_track(self):
        """Selects and plays a random track that hasn't been played recently"""
        import random
        
        # Get tracks that haven't been played yet
        available = [track for track in self.available_tracks if track not in self.played_tracks]
        
        # If all tracks have been played, reset
        if not available:
            self.played_tracks = [self.current_track] if self.current_track else []
            available = [track for track in self.available_tracks if track not in self.played_tracks]
        
        # Select a random track from available ones
        self.current_track = random.choice(available)
        
        # Add to played tracks
        self.played_tracks.append(self.current_track)
        
        # Keep track of last 3 tracks only
        if len(self.played_tracks) > 3:
            self.played_tracks.pop(0)
        
        # Play the track
        try:
            pygame.mixer.music.load(self.current_track)
            pygame.mixer.music.play()  # Play once without looping
            self.add_game_event(f"Now playing: {self.current_track}")
        except Exception as e:
            print(f"Error playing music: {e}")

    
    def stop_music(self):
        """Stops the current music track"""
        try:
            pygame.mixer.music.stop()
        except Exception as e:
            print(f"Error stopping music: {e}")
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.disconnect()

    def gameStart(self, app_client):
        self.active_view = "game"
        self.game_events = []
        self.counting = True
        self.running = False
        self.gameOver = False
        self.last_processed_i = 0

        self.update_server_info()

        self.countDown = 30.0
    
        fps = 60.0
        self.timer = 6.0 * 60 +.99

        for team in [self.red_team, self.green_team]:
            for player in team:
                player.score = 0

        self.add_game_event("Game countdown started...")

    '''
    F5>30 minute countdown>Send 202 to UDP port 7500>
    Equipment begins accepting input and transmitting data
    '''
    
    def gameUpdate(self, app_client):
        fps = 60
        if self.counting:
            self.countDown -= 1 /fps

            if abs(self.countDown - 17.0) < 1/fps and not pygame.mixer.music.get_busy():
                self.play_random_track()
                self.add_game_event(f"Now playing: {self.current_track}" )
                
            if self.countDown <= 0:
                self.counting = False
                self.running = True
                try:
                    app_client.send_message('202')
                    print("Code 202 Sent")
                    self.add_game_event("Game started!")
                except Exception as e:
                    print(f"Error sending game start code: {e}")
            elif int(self.countDown) % 10 == 0 and abs(self.countDown - int(self.countDown)) < 0.01:
                self.add_game_event(f"Game starts in {int(self.countDown)} seconds...")
        elif self.running:
            try:

                #Process incoming hit data.  Checks for new hit data, calculates score, updates gamestate with new events and scores
                self.process_data(app_client)
                
                self.timer -= 1/fps

                # if music stops, play a new track
                if not pygame.mixer.music.get_busy():
                    self.play_random_track()
                    
                if self.timer <= 0:
                    self.running = False
                    self.gameOver = True

                    for _ in range(3):
                        app_client.send_message('221')
                        print("Code 221 Sent")
                    self.add_game_event("Game over!")

                    self.stop_music()

                elif self.timer <= 30 * fps and self.timer > (30 * fps - fps):
                    self.add_game_event("30 Seconds Left!")
            except:
                print("Running Error")
                self.timer = 6.0*60
        
    #add event message to game event list
    def add_game_event(self, eventmsg):
        self.game_events.append(eventmsg)
        if len(self.game_events) > 50:
            self.game_events.pop(0)

    #Synchronizes current team info with the server, allows server to know which equiipment ID is with which team.
    def update_server_info(self):
        server = get_app_server()
        if server and hasattr(server, 'update_team_info'):
            server.update_team_info(self.red_team, self.green_team)

    #Some quick helper functions

    def find_player_by_eID(self, e_id):
        for team in [self.red_team, self.green_team]:
            for player in team:
                if player.equipment_id == e_id:
                    return player
        return None
    
    def get_player_team(self, player):
        for p in self.red_team:
            if p == player:
                return 'red'
        return 'green'

    '''
    Listen on 7501, record hits into recieved_data
    Checks for hits, processes shooter & target, updates scores, generates game events
    '''
    def process_data(self, app_client):
        try:
            server = get_app_server()
            if not server:
                return
            
            recievedData = server.get_data()
            if not recievedData:
                return
            
            if not hasattr(self, 'last_processed_i'):
                self.last_processed_i = 0
            
            new_data = recievedData[self.last_processed_i:]
            if not new_data:
                return
            
            self.last_processed_i = len(recievedData)

            for s_eid, t_eid in new_data:
                shooter = self.find_player_by_eID(s_eid)
                target = self.find_player_by_eID(t_eid)

                if shooter and target:
                    shooterTeam = self.get_player_team(shooter)
                    targetTeam = self.get_player_team(target)

                    if shooterTeam == targetTeam:
                        shooter.score -= 10
                        self.add_game_event(f"{shooterTeam.capitalize()} player {shooter.codename} hit teammate {target.codename}! -10 points")
                    else:
                        shooter.score += 10
                        self.add_game_event(f"{shooterTeam.capitalize()} player {shooter.codename} hit {targetTeam} player {target.codename}! + 10 points")
        except Exception as e:
            print(f"Error processing: {str(e)}")

def get_app_client():
    return app_client

def get_app_server():
    return app_server
