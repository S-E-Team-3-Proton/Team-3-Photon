import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 127, 0)
GRAY = (128, 128, 128)

FONT = None
TITLE_FONT = None
BUTTON_FONT = None

def font_init(font, titlefont, button_font):
    global FONT, TITLE_FONT, BUTTON_FONT
    FONT = font
    TITLE_FONT = titlefont
    BUTTON_FONT = button_font

def draw_view(screen, game_state):
    if game_state.active_view == "entry":
        draw_entry_screen(screen, game_state)
    elif game_state.active_view == "parameters":
        draw_parameters_screen(screen, game_state)
    elif game_state.active_view == "game":
        draw_game_screen(screen, game_state)


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


    screen.blit(red_header, (red_header_x, 57))
    screen.blit(green_header, (green_header_x, 57))


    field_names = ["p_id","e_id","name"]
    f_widths=[100,100,150] # width of the box
    spacing = 10 # space between boxes

    total_width = sum(f_widths) + spacing * 2 # spacing between three boxes.

    x_redP = SCREEN_WIDTH // 4 - total_width // 2
    x_greenP = SCREEN_WIDTH * 3 // 4 - total_width // 2

    
    # Draw field headers
    for i, field in enumerate(field_names):
        x_red = x_redP
        x_green = x_greenP
        
        # width of previous boxes plus spacing
        for j in range(i):
            x_red += f_widths[j] + spacing
            x_green += f_widths[j] + spacing
            
        field_header = FONT.render(field, True, WHITE)
        screen.blit(field_header, (x_red + (f_widths[i] - field_header.get_width()) // 2, 80))
        screen.blit(field_header, (x_green + (f_widths[i] - field_header.get_width()) // 2, 80))

    

    
    # Draw player slots with rounded corners & shadow
    for i in range(15):
        y_pos = 110 + i * 30
        draw_playerInfo(screen, game_state, game_state.red_team[i], x_redP, y_pos, f_widths, spacing, "red", i)
        draw_playerInfo(screen, game_state, game_state.green_team[i], x_greenP, y_pos, f_widths, spacing, "green", i)


    # calculate button centering
    button_width = 130
    button_spacing = 10  # Space between buttons
    total_buttons = 5
    total_width = button_width * total_buttons + button_spacing * (total_buttons - 1)
    start_x = SCREEN_WIDTH // 2 - total_width // 2  # Center all buttons


    # draw buttons centered in team area
    draw_button(screen, "F1 - Edit Game", start_x, SCREEN_HEIGHT - 70)
    draw_button(screen, "F2 - Game Parameters", start_x + button_width + button_spacing, SCREEN_HEIGHT - 70)
    draw_button(screen, "F5 - Start Game", start_x + 2 * (button_width + button_spacing), SCREEN_HEIGHT - 70)
    draw_button(screen, "F7 - New Game", start_x + 3 * (button_width + button_spacing), SCREEN_HEIGHT - 70)
    draw_button(screen, "F12 - Clear Game", start_x + 4 * (button_width + button_spacing), SCREEN_HEIGHT - 70)


def draw_playerInfo(screen, game_state, player, x, y, f_widths, spacing, team, index):
    field_vals = [
        str(player.player_id) if player.player_id else "", 
        str(player.equipment_id) if player.equipment_id else "",
        player.codename if player.codename else ""
    ]
    
    field_names = ["p_id","e_id","name"]
    fieldColor = RED if team == "red" else GREEN

    for i, val in enumerate(field_vals):
        x_pos = x
        for j in range(i):
            x_pos += f_widths[j] + spacing 

        f_width = f_widths[i]  

        pygame.draw.rect(screen, (20, 20, 20), (x_pos + 3, y + 3, f_width, 25), border_radius=6)
        pygame.draw.rect(screen, fieldColor, (x_pos, y, f_width, 25), border_radius=6)


        active = (game_state.current_team == team
                  and game_state.current_index == index
                  and game_state.active_input == field_names[i]
                )
        
        if active:
            pygame.draw.rect(screen, WHITE, (x_pos - 2, y - 2, f_width + 4, 29),3, border_radius=8)
            pygame.draw.rect(screen, BLACK, (x_pos, y, f_width, 25),3, border_radius=6)

            textInsert = game_state.input_text if game_state.input_text else F"Enter {field_names[i]}"
            text_S = FONT.render(textInsert, True, WHITE)
        else:
            text_S = FONT.render(val, True, WHITE)

        if i < 2:
            textXPos = x_pos + (f_width-text_S.get_width()) // 2
        else:
            textXPos = x_pos + 5

        text_height = text_S.get_height()
        text_y = y + (25 - text_height) // 2 
        screen.blit(text_S, (textXPos, text_y))


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
    #button_area_end = SCREEN_WIDTH * 3 // 4 - 150 + 300  # Right boundary
    #button_area_width = button_area_end - button_area_start  # Total width

    # calculate button centering
    button_width = 130
    button_spacing = 10  # Space between buttons
    total_buttons = 4
    total_width = button_width * total_buttons + button_spacing * (total_buttons - 1)
    start_x = SCREEN_WIDTH // 2 - total_width // 2  # Center all buttons

    # draw buttons centered at the bottom of the screen
    draw_button(screen, "F1 - Edit Game", start_x, SCREEN_HEIGHT - 70)
    draw_button(screen, "F2 - Game Parameters", start_x + (button_width + button_spacing), SCREEN_HEIGHT - 70)
    draw_button(screen, "F5 - Start Game", start_x + 2 * (button_width + button_spacing), SCREEN_HEIGHT - 70)
    draw_button(screen, "F7 - New Game", start_x + 3 * (button_width + button_spacing), SCREEN_HEIGHT - 70)
    
def draw_button(screen, text, x, y):
    button_rect = pygame.Rect(x, y, 130, 40) 
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

def draw_game_screen(screen, game_state):
    SCREEN_HEIGHT = screen.get_height()
    SCREEN_WIDTH = screen.get_width()
    for i in range(SCREEN_HEIGHT):
        pygame.draw.line(screen, (30, 30, 30), (0, i), (SCREEN_WIDTH, i), 1)  
    
    #game action display main title 
    title_shadow = TITLE_FONT.render("Game Action Screen", True, (50, 50, 50))
    title_shadow_x = SCREEN_WIDTH // 2 - title_shadow.get_width() // 2
    title_y = 20  # Consistent Y-value for alignment
    screen.blit(title_shadow, (title_shadow_x + 2, title_y + 2))
    title = TITLE_FONT.render("Game Action Screen", True, WHITE)
    title_x = SCREEN_WIDTH // 2 - title.get_width() // 2
    screen.blit(title, (title_x, title_y))
    #calculate team scores
    red_score = sum(player.score for player in game_state.red_team if hasattr(player, 'score'))
    green_score = sum(player.score for player in game_state.green_team if hasattr(player, 'score'))
    #determine flashing color
    flash_color = RED if red_score > green_score else GREEN if green_score > red_score else WHITE
    if game_state.timer % 30 < 15 and (red_score != green_score):
        flash_color = WHITE
    #vertical alignment for red/green team 
    team_header_y = title_y
    score_y = team_header_y + 35
    #equal horizontal spacing from center
    spacing = 300
    center_x = SCREEN_WIDTH // 2
    #Red team header and score for game event screen
    red_color = flash_color if red_score > green_score else RED
    red_x = center_x - spacing
    red_header = TITLE_FONT.render("RED TEAM", True, red_color)
    red_score_text = TITLE_FONT.render(str(red_score), True, red_color)
    screen.blit(red_header, (red_x - red_header.get_width() // 2, team_header_y))
    screen.blit(red_score_text, (red_x - red_score_text.get_width() // 2, score_y))
    #Green team header for game event screen
    green_color = flash_color if green_score > red_score else GREEN
    green_x = center_x + spacing
    green_header = TITLE_FONT.render("GREEN TEAM", True, green_color)
    green_score_text = TITLE_FONT.render(str(green_score), True, green_color)
    screen.blit(green_header, (green_x - green_header.get_width() // 2, team_header_y))
    screen.blit(green_score_text, (green_x - green_score_text.get_width() // 2, score_y))
    #Blue display box for game event screen
    p_width = SCREEN_WIDTH - 100
    centrPoint = (SCREEN_WIDTH - p_width) // 2
    pygame.draw.rect(screen, (0,0,100), (centrPoint, 90, p_width, 200), border_radius=10)
    pygame.draw.rect(screen, (0,0,150), (centrPoint, 90, p_width, 30), border_radius=10)
    event_head = FONT.render("Current Actions", True, WHITE)
    screen.blit(event_head,(SCREEN_WIDTH//2 - event_head.get_width()//2, 95))
    #display game event messages
    yoffset = 125
    for event in game_state.game_events[-8:]:
        etext = FONT.render(event, True, WHITE)
        screen.blit(etext, (SCREEN_WIDTH // 2 - 340, yoffset))
        yoffset += 20
    #player scores for each team
    drawScores(screen, game_state.red_team, SCREEN_WIDTH//4 -125, 350, RED)
    drawScores(screen, game_state.green_team, SCREEN_WIDTH*3//4 -125, 350, GREEN)

    if game_state.counting:
        timer_text = f"Starting in: {int(game_state.countDown)} seconds"
    else:
        try:
            minutes = int(game_state.timer) // 60
            seconds = int(game_state.timer) % 60
            timer_text = f"Time Remaining: {minutes:01d}:{seconds:02d}"
        except Exception as e:
            timer_text = "Time Remaining: 6:00"
    
    timer_display = TITLE_FONT.render(timer_text, True, WHITE)
    screen.blit(timer_display, (SCREEN_WIDTH // 2 - timer_display.get_width() // 2, SCREEN_HEIGHT - 60))

    if game_state.gameOver:
        draw_button(screen, "F1 - Player Entry", SCREEN_WIDTH // 2 - 65, SCREEN_HEIGHT - 100)

def drawScores(screen, team, x, y, color):
    valid_players = []
    for player in team:
        if hasattr(player, 'score') and player.player_id:
            valid_players.append(player)
            
    playersByScore = sorted(valid_players, key=lambda p: p.score, reverse=True)
    
    pygame.draw.rect(screen, color, (x, y, 250, 30), border_radius=6)
    header = FONT.render("Player Scores", True, WHITE)
    screen.blit(header, (x + 125 - header.get_width() // 2, y + 5))

    backgrColor = (30,30,30)
    yoffset= y+35

    for i, player in enumerate(playersByScore):
        if player.player_id:
            pygame.draw.rect(screen, backgrColor, (x,yoffset,250,25), border_radius=4)

            p_name = f"{player.codename}"
            p_score = getattr(player,'score',0)

            name_bckg = FONT.render(p_name, True, WHITE)
            score_bckg = FONT.render(str(p_score), True, WHITE)
            
            screen.blit(name_bckg, (x + 10, yoffset + 5))
            screen.blit(score_bckg, (x + 240 - score_bckg.get_width(), yoffset + 5))
            
            yoffset += 30
            
            if i >= 7:
                break


    
