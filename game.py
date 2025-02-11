import pygame
import time
import psycopg2

pygame.init()
pygame.font.init()

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Laser Tag Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)


# Fonts
FONT = pygame.font.SysFont('Arial', 20)
TITLE_FONT = pygame.font.SysFont('Arial', 24, bold=True)
BUTTON_FONT = pygame.font.SysFont('Arial', 14)  


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
        self.active_input = None
        self.input_text = ""
        self.db_connection = None
        self.connect_to_db()

    def connect_to_db(self):
        try:
            self.db_connection = psycopg2.connect(
                dbname="photon",
                user="student",  
                password="student",
                host="localhost"
            )
        except psycopg2.Error as e:
            print(f"Database connection error: {e}")

    def query_codename(self, player_id):
        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute("SELECT codename FROM players WHERE id = %s", (player_id,))
                result = cursor.fetchone()
                return result[0] if result else None
            except psycopg2.Error as e:
                print(f"Database query error: {e}")
                return None
        return None

     def add_new_player(self, player_id, codename):
        """Inserts a new player into the database."""
        if not player_id.strip().isdigit() or not codename.strip():
            return  # Prevent invalid inputs
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "INSERT INTO players (id, codename) VALUES (%s, %s)",
                (int(player_id), codename)
            )
            self.db_connection.commit()
        except psycopg2.Error as e:
            print(f"Database insert error: {e}")


def draw_entry_screen(screen, game_state):
    # gradient background
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

        # Rounded slots
        pygame.draw.rect(screen, RED, (x_red, y_pos, 300, 25), border_radius=6)
        pygame.draw.rect(screen, GREEN, (x_green, y_pos, 300, 25), border_radius=6)

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


        # Render the correct prompt
        input_surface = FONT.render(game_state.input_text if game_state.input_text else prompt_text, True, WHITE)

        screen.blit(input_surface, (x_pos + 5, y_pos + 5))


    # Calculate button from Red Team start to Green Team end
    button_area_start = x_red  # Left boundary (Red Team start)
    button_area_end = x_green + 300  # Right boundary (Green Team end)
    button_area_width = button_area_end - button_area_start  # Total width

    # calculate button centering
    button_width = 90
    button_spacing = 40  # Space between buttons
    total_button_width = 5 * button_width + 4 * button_spacing  # Total width of all buttons
    start_x = button_area_start + (button_area_width - total_button_width) // 2  # Center within team area


    # draw buttons centered in team area
    draw_button(screen, "F1 - Edit Game", start_x, SCREEN_HEIGHT - 70)
    draw_button(screen, "F2 - Game Parameters", start_x + button_width + button_spacing, SCREEN_HEIGHT - 70)
    draw_button(screen, "F3 - Start Game", start_x + 2 * (button_width + button_spacing), SCREEN_HEIGHT - 70)
    draw_button(screen, "F7 - New Game", start_x + 3 * (button_width + button_spacing), SCREEN_HEIGHT - 70)
    draw_button(screen, "F12 - Clear Game", start_x + 4 * (button_width + button_spacing), SCREEN_HEIGHT - 70)


def draw_button(screen, text, x, y):
    button_rect = pygame.Rect(x, y, 180, 40) 
    pygame.draw.rect(screen, GRAY, button_rect, border_radius=8)

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
        if event.key == pygame.K_DOWN:
            game_state.current_index = (game_state.current_index + 1) % 15  # Move down the list
        elif event.key == pygame.K_UP:
            game_state.current_index = (game_state.current_index - 1) % 15  # Move up the list

        if event.key == pygame.K_F12:  # Clear game
            game_state.red_team = [Player() for _ in range(15)]
            game_state.green_team = [Player() for _ in range(15)]
            game_state.current_index = 0
            game_state.active_input = None
        elif event.key == pygame.K_F3:  # Start game
            # Implement transition to game screen
            pass
        elif event.key == pygame.K_TAB:  # Switch teams
            game_state.current_team = "green" if game_state.current_team == "red" else "red"
        elif game_state.active_input:
            if event.key == pygame.K_RETURN:
                if game_state.active_input == "player_id":
                    if game_state.input_text.strip().isdigit():  # Ensure player_id is a valid number
                        player_id = game_state.input_text.strip()
                        game_state.current_player_id = player_id  # Store player_id safely

                        codename = game_state.query_codename(player_id)  # Query database for existing codename
                        current_team = game_state.red_team if game_state.current_team == "red" else game_state.green_team
                        current_team[game_state.current_index].player_id = player_id  # Store in player object

                        if codename:
                            current_team[game_state.current_index].codename = codename
                            game_state.active_input = "equipment_id"  # Move to equipment entry
                        else:
                            game_state.active_input = "new_codename"  # Ask for a new codename
                    else:
                        print("⚠️ Invalid Player ID! Please enter a valid number.")
                    
                    game_state.input_text = ""  # Clear input box

                elif game_state.active_input == "equipment_id":
                    current_team = game_state.red_team if game_state.current_team == "red" else game_state.green_team
                    current_team[game_state.current_index].equipment_id = game_state.input_text
                    game_state.current_index += 1
                    game_state.active_input = None
                    game_state.input_text = ""
                elif game_state.active_input == "new_codename":
                    current_team = game_state.red_team if game_state.current_team == "red" else game_state.green_team
                    player_id = current_team[game_state.current_index].player_id
                    game_state.add_new_player(player_id, game_state.input_text)
                    current_team[game_state.current_index].codename = game_state.input_text
                    game_state.active_input = "equipment_id"
                    game_state.input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                game_state.input_text = game_state.input_text[:-1]
            else:
                game_state.input_text += event.unicode
        elif event.key == pygame.K_RETURN:  # Start new player entry
            if game_state.current_index < 15:
                game_state.active_input = "player_id"

def main_game_loop():
    # Splash screen
    photon_logo = pygame.image.load("logo.jpg")
    photon_logo = pygame.transform.scale(photon_logo, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(photon_logo, (0, 0))
    pygame.display.update()
    time.sleep(3)  # Display splash screen for 3 seconds
    
    # Initialize game state
    game_state = GameState()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            handle_event(event, game_state)
        
        draw_entry_screen(screen, game_state)
        pygame.display.update()
    
    if game_state.db_connection:
        game_state.db_connection.close()
    pygame.quit()

if __name__ == "__main__":
    main_game_loop()
