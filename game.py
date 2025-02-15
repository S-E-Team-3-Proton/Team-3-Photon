import pygame
from photon_db import PDB
from client import UDPClient
from server import UDPServer

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

def init_game():
    global FONT, TITLE_FONT, BUTTON_FONT, app_client, app_server
    FONT = pygame.font.SysFont('Arial', 20)
    TITLE_FONT = pygame.font.SysFont('Arial', 24, bold=True)
    BUTTON_FONT = pygame.font.SysFont('Arial', 14)
    app_client = UDPClient("127.0.0.1") #default 
    app_server = UDPServer("127.0.0.1") #default
    app_server.start()

class Player:
    def __init__(self, player_id="", codename="", equipment_id=None):
        self.player_id = player_id
        self.codename = codename
        self.equipment_id = int(equipment_id) if equipment_id and equipment_id.isdigit() else 0

class GameState:
    def __init__(self):
        self.red_team = [Player() for _ in range(15)]
        self.green_team = [Player() for _ in range(15)]
        self.current_team = "red"  
        self.current_index = 0
        self.active_input = "player_id"
        self.previous_inpput = None
        self.input_text = ""
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
        
        return self.db.add_player(int(player_id), codename)
    
    def assign_equipment(self, player_id, equipment_id):
        if not player_id.strip().isdigit() or not equipment_id.strip().isdigit():
            return False
        return self.db.set_EquipID(int(player_id), int(equipment_id))
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.disconnect()

def draw_view(screen, game_state):
    if game_state.active_view == "entry":
        draw_entry_screen(screen, game_state)
    elif game_state.active_view == "parameters":
        draw_parameters_screen(screen, game_state)

def draw_entry_screen(screen, game_state):
    # gradient background
    SCREEN_HEIGHT = screen.get_height()
    SCREEN_WIDTH = screen.get_width()
    for i in range(SCREEN_HEIGHT):
        pygame.draw.line(screen, (30, 30, 30), (0, i), (SCREEN_WIDTH, i), 1)  

    # Draw title with shadow
    title_shadow = TITLE_FONT.render("Edit Current Game", True, (50, 50, 50))
    screen.blit(title_shadow, (SCREEN_WIDTH // 2 - title_shadow.get_width() // 2 + 2, 22))
    title = TITLE_FONT.render("Edit Current Game", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))
    
    # Draw team headers
    red_header = TITLE_FONT.render("RED TEAM", True, RED)
    green_header = TITLE_FONT.render("GREEN TEAM", True, GREEN)
    # Center team headers dynamically
    red_header_x = SCREEN_WIDTH // 4 - red_header.get_width() // 2
    green_header_x = SCREEN_WIDTH * 3 // 4 - green_header.get_width() // 2


    screen.blit(red_header, (red_header_x, 60))
    screen.blit(green_header, (green_header_x, 60))

    
    # Draw player slots with rounded corners & shadow
    for i in range(15):
        x_red = SCREEN_WIDTH // 4 - 150  # Center Red Team
        x_green = SCREEN_WIDTH * 3 // 4 - 150  # Center Green Team
        y_pos = 100 + i * 30

        # Shadow effect
        pygame.draw.rect(screen, (20, 20, 20), (x_red + 3, y_pos + 3, 300, 25), border_radius=6)
        pygame.draw.rect(screen, (20, 20, 20), (x_green + 3, y_pos + 3, 300, 25), border_radius=6)
        pygame.draw.rect(screen, RED, (x_red, y_pos, 300, 25), border_radius=6)
        pygame.draw.rect(screen, GREEN, (x_green, y_pos, 300, 25), border_radius=6)
        # pygame.draw.rect(screen, (20, 20, 20), (x_red + 3, y_pos + 3, 300, 25))
        # pygame.draw.rect(screen, (20, 20, 20), (x_green + 3, y_pos + 3, 300, 25))
        # pygame.draw.rect(screen, RED, (x_red, y_pos, 300, 25))
        # pygame.draw.rect(screen, GREEN, (x_green, y_pos, 300, 25))

        # Display player names
        if game_state.red_team[i].codename:
            text = FONT.render(f"{game_state.red_team[i].codename}", True, WHITE)
            screen.blit(text, (x_red + 10, y_pos + 5))
            
        if game_state.green_team[i].codename:
            text = FONT.render(f"{game_state.green_team[i].codename}", True, WHITE)
            screen.blit(text, (x_green + 10, y_pos + 5))

    # Highlight active input slot with glowing effect
    if game_state.active_input:
        x_pos = 50 if game_state.current_team == "red" else 450
        y_pos = 100 + game_state.current_index * 30  

        pygame.draw.rect(screen, WHITE, (x_pos - 2, y_pos - 2, 304, 29), 3, border_radius=8)
        # pygame.draw.rect(screen, WHITE, (x_pos - 2, y_pos - 2, 304, 29), 3)

     
      
        # Determine prompt text based on input phase
        if game_state.active_input == "player_id":
            prompt_text = "Enter Player ID:"
        elif game_state.active_input == "equipment_id":
            prompt_text = "Enter Equipment ID:"
        elif game_state.active_input == "new_codename":
            prompt_text = "Enter New Codename:"
        else:
            prompt_text = "Enter Data..."
        
        pygame.draw.rect(screen, BLACK, (x_pos, y_pos, 300, 25), border_radius=6)  # Overwrite slot with black
        # pygame.draw.rect(screen, BLACK, (x_pos, y_pos, 300, 25))


        # Render the correct prompt
        input_surface = FONT.render(game_state.input_text if game_state.input_text else prompt_text, True, WHITE)

        screen.blit(input_surface, (x_pos + 5, y_pos + 5))


    # Calculate button from Red Team start to Green Team end
    button_area_start = x_red  # Left boundary (Red Team start)
    #button_area_end = x_green + 300  # Right boundary (Green Team end)
    #button_area_width = button_area_end - button_area_start  # Total width

    # calculate button centering
    button_width = 90
    button_spacing = 40  # Space between buttons
    #total_button_width = 5 * button_width + 4 * button_spacing  # Total width of all buttons
    #start_x = button_area_start + (button_area_width - total_button_width) // 2  # Center within team area
    start_x = button_area_start


    # draw buttons centered in team area
    draw_button(screen, "F1 - Edit Game", start_x, SCREEN_HEIGHT - 70)
    draw_button(screen, "F2 - Game Parameters", start_x + button_width + button_spacing, SCREEN_HEIGHT - 70)
    draw_button(screen, "F3 - Start Game", start_x + 2 * (button_width + button_spacing), SCREEN_HEIGHT - 70)
    draw_button(screen, "F7 - New Game", start_x + 3 * (button_width + button_spacing), SCREEN_HEIGHT - 70)
    draw_button(screen, "F12 - Clear Game", start_x + 4 * (button_width + button_spacing), SCREEN_HEIGHT - 70)

def draw_parameters_screen(screen, game_state):
    # gradient background
    SCREEN_HEIGHT = screen.get_height()
    SCREEN_WIDTH = screen.get_width()
    for i in range(SCREEN_HEIGHT):
        pygame.draw.line(screen, (30, 30, 30), (0, i), (SCREEN_WIDTH, i), 1)  

    # Draw title with shadow
    title_shadow = TITLE_FONT.render("Edit Game Parameters", True, (50, 50, 50))
    screen.blit(title_shadow, (SCREEN_WIDTH // 2 - title_shadow.get_width() // 2 + 2, 22))
    title = TITLE_FONT.render("Edit Game Parameters", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

    # Draw network address change text
    net_option_shadow = FONT.render("Change Network Address", True, (50, 50, 50))
    screen.blit(net_option_shadow, (SCREEN_WIDTH // 2 - net_option_shadow.get_width() // 2 + 2, 102))
    net_option = FONT.render("Change Network Address", True, WHITE)
    screen.blit(net_option, (SCREEN_WIDTH // 2 - net_option.get_width() // 2, 100))

    # Draw rectangle for entering text
    pygame.draw.rect(screen, (20, 20, 20), (SCREEN_WIDTH // 2 - 150 + 3, 130 + 3, 300, 25), border_radius=6)
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 150, 130, 304, 29), 3, border_radius=6)
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 -150 + 2 , 130 + 2, 300, 25), border_radius=6)

    # Render text prompting in box
    input_surface = FONT.render(game_state.input_text if game_state.input_text else "Enter IP:", True, WHITE)
    screen.blit(input_surface, (SCREEN_WIDTH // 2 -150 + 2 + 5, 130 + 5))

    # Calculate button from Red Team start to Green Team end
    button_area_start = SCREEN_WIDTH // 4 - 150  # Left boundary 
    #button_area_end = SCREEN_WIDTH * 3 // 4 - 150 + 300  # Right boundary
    #button_area_width = button_area_end - button_area_start  # Total width

    # calculate button centering
    button_width = 90
    button_spacing = 40  # Space between buttons
    #total_button_width = 5 * button_width + 4 * button_spacing  # Total width of all buttons
    #start_x = button_area_start + (button_area_width - total_button_width) // 2  # Center within team area
    start_x = button_area_start

    # draw buttons centered in team area at the bottom of the screen
    draw_button(screen, "F1 - Edit Game", start_x, SCREEN_HEIGHT - 70)
    draw_button(screen, "F2 - Game Parameters", start_x + button_width + button_spacing, SCREEN_HEIGHT - 70)
    draw_button(screen, "F3 - Start Game", start_x + 2 * (button_width + button_spacing), SCREEN_HEIGHT - 70)
    draw_button(screen, "F7 - New Game", start_x + 3 * (button_width + button_spacing), SCREEN_HEIGHT - 70)
    

def draw_button(screen, text, x, y):
    button_rect = pygame.Rect(x, y, 180, 40) 
    pygame.draw.rect(screen, GRAY, button_rect, border_radius=8)
    # pygame.draw.rect(screen, GRAY, button_rect)

    # Split text into two lines if it's too long
    words = text.split(" ")
    if len(words) > 2:  # If text is too long, break into two lines
        first_line = " ".join(words[:2])
        second_line = " ".join(words[2:])
        button_text1 = BUTTON_FONT.render(first_line, True, WHITE)
        button_text2 = BUTTON_FONT.render(second_line, True, WHITE)
        screen.blit(button_text1, (x + 10, y + 5))
        screen.blit(button_text2, (x + 10, y + 25))
    else:
        button_text = BUTTON_FONT.render(text, True, WHITE)
        screen.blit(button_text, (x + 10, y + 15))  # Centered vertically

def handle_event(event, game_state):
    if event.type == pygame.KEYDOWN:
        if game_state.active_view == "entry":
            if game_state.active_input == "player_id":
                if event.key == pygame.K_DOWN:
                    game_state.current_index = (game_state.current_index + 1) % 15  # Move down the list
                elif event.key == pygame.K_UP:
                    game_state.current_index = (game_state.current_index - 1) % 15  # Move up the list

            if event.key == pygame.K_F12:  # Clear game
                game_state.red_team = [Player() for _ in range(15)]
                game_state.green_team = [Player() for _ in range(15)]
                game_state.current_index = 0
                game_state.active_input = "player_id"
                game_state.db.reset_EquipID()
            elif event.key == pygame.K_F3:  # Start game
                # Implement transition to game screen
                pass
            elif event.key == pygame.K_F2: # Switch to game parameters screen (change network address here)
                game_state.active_view = "parameters"
                game_state.previous_input = game_state.active_input
                game_state.active_input = "ip_address"
            elif event.key == pygame.K_TAB and game_state.active_input == "player_id":  # Switch teams
                game_state.current_team = "green" if game_state.current_team == "red" else "red"
            elif game_state.active_input:
                if event.key == pygame.K_RETURN:
                    current_team = game_state.red_team if game_state.current_team == "red" else game_state.green_team

                    if game_state.active_input == "player_id":
                        if game_state.input_text.strip().isdigit():  # Ensure player_id is a valid number
                            player_id = game_state.input_text.strip()
                            game_state.current_player_id = player_id  # Store player_id safely

                            codename = game_state.query_codename(player_id)  # Query database for existing codename
                            current_team[game_state.current_index].player_id = player_id  # Store in player object

                            if codename:
                                current_team[game_state.current_index].codename = codename
                                game_state.active_input = "equipment_id"  # Move to equipment entry
                            else:
                                game_state.active_input = "new_codename"  # Ask for a new codename
                        else:
                            print("⚠️ Invalid Player ID! Please enter a valid number.")
                        

                    elif game_state.active_input == "equipment_id":
                        if game_state.input_text.strip().isdigit():
                            equipment_id = game_state.input_text.strip()
                            #transmit the equipment id via app_client to generator server
                            app_client.send_message(equipment_id)
                            if game_state.assign_equipment(current_team[game_state.current_index].player_id, equipment_id):
                                current_team[game_state.current_index].equipment_id = equipment_id
                                game_state.current_index += 1
                                game_state.active_input = "player_id"
                            else:
                                print("⚠️ Equipment ID already in use!")
                        else:
                            print("⚠️ Invalid Equipment ID!")

                    elif game_state.active_input == "new_codename":
                        if game_state.input_text.strip():
                            codename = game_state.input_text.strip()
                            if game_state.add_new_player(game_state.current_player_id, codename):
                                current_team[game_state.current_index].codename = codename
                                game_state.active_input = "equipment_id"
                            else:
                                print("⚠️ Failed to add player!")
                        else:
                            print("⚠️ Invalid Codename!")

                    game_state.input_text = ""  # Clear input box
                elif event.key == pygame.K_BACKSPACE:
                    game_state.input_text = game_state.input_text[:-1]
                elif event.key == pygame.K_TAB and game_state.active_input == "new_codename":
                    return
                elif event.key == pygame.K_TAB and game_state.active_input == "equipment_id":
                    return
                else:
                    game_state.input_text += event.unicode
            # elif event.key == pygame.K_RETURN:  # Start new player entry
            #     if game_state.current_index < 15:
            #         game_state.active_input = "player_id"
        elif game_state.active_view == "parameters":
            if event.key == pygame.K_F1:  # Change to edit game
                game_state.active_view = "entry"
                game_state.active_input = game_state.previous_input
            elif event.key == pygame.K_F3:  # Start game
                # Implement transition to game screen
                pass
            elif event.key == pygame.K_RETURN:  # Start network address entry
                if game_state.input_text.strip():
                    new_ip_address = game_state.input_text.strip()
                    app_client.set_network_address(new_ip_address)
                    app_server.set_network_address(new_ip_address)
                    game_state.active_input = None
                else:
                    print("⚠️ Invalid Network Address!")
                game_state.input_text = ""  # Clear input box
            elif event.key == pygame.K_BACKSPACE:
                game_state.input_text = game_state.input_text[:-1]
            else:
                game_state.input_text += event.unicode
