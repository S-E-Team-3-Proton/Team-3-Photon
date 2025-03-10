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

def get_app_client():
    return app_client

def get_app_server():
    return app_server
