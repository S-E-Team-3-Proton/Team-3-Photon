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


def init_game():
    global FONT, TITLE_FONT, BUTTON_FONT, app_client, app_server
    FONT = pygame.font.SysFont('Arial', 20)
    TITLE_FONT = pygame.font.SysFont('Arial', 24, bold=True)
    BUTTON_FONT = pygame.font.SysFont('Arial', 14)

    render.font_init(FONT, TITLE_FONT, BUTTON_FONT)

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
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.disconnect()


    def gameStart(self, app_client):
        self.active_view = "game"
        self.game_events = []
        self.counting = True
        self.running = False
        self.gameOver = False

        self.countDown = 30.0
    
        fps = 60.0
        self.timer = 6.0 * 60 +.99

        for team in [self.red_team, self.green_team]:
            for player in team:
                player.score = 0

        self.add_game_event("Game countdown started...")

    def gameUpdate(self, app_client):
        fps = 60
        if self.counting:
            self.countDown -= 1 /fps
            if self.countDown <= 0:
                self.counting = False
                self.running = True
                try:
                    app_client.send_message('202')
                    app_client.send_message('202')
                    app_client.send_message('202')
                    self.add_game_event("Game started! Code 202 sent.")
                except Exception as e:
                    print(f"Error sending game start code: {e}")
            elif int(self.countDown) % 10 == 0 and abs(self.countDown - int(self.countDown)) < 0.01:
                self.add_game_event(f"Game starts in {int(self.countDown)} seconds...")
        elif self.running:
            try:
                self.timer -= 1/fps
                if self.timer <= 0:
                    self.running = False
                    self.gameOver = True

                    for _ in range(3):
                        app_client.send_message('221')
                    self.add_game_event("Game over! Code 221 sent.")

                elif self.timer <= 30 * fps and self.timer > (30 * fps - fps):
                    self.add_game_event("30 Seconds Left!")
            except:
                print("Running Error")
                self.timer = 6.0*60
        

    def add_game_event(self, eventmsg):
        self.game_events.append(eventmsg)
        if len(self.game_events) > 50:
            self.game_events.pop(0)


def get_app_client():
    return app_client

def get_app_server():
    return app_server
