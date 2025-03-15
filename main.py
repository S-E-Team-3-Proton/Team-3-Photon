import pygame
from game import init_game, GameState, handle_event
from render import draw_view
from event_handler import handle_event

def main():

    pygame.init()
    pygame.font.init()

    init_game()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 650
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Laser Tag Game")

    try:
        photon_logo = pygame.image.load("logo.jpg")
        photon_logo = pygame.transform.scale(photon_logo, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(photon_logo, (0, 0))
        pygame.display.update()
        pygame.time.wait(3000)  # Display splash screen for 3 seconds
    except:
        print("Couldn't load splash screen")
    
    # Initialize game state
    game_state = GameState()
    app_client = get_app_client()
    app_server = get_app_server()

    clock = pygame.time.Clock()
    running = True
    last_update_time = pygame.time.get_ticks()
    
    while running:

        current_time = pygame.time.get_ticks()
        dt = current_time - last_update_time
        last_update_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            handle_event(event, game_state, app_client,app_server)
        
        if game_state.active_view == "game":
            game_state.gameUpdate(app_client)

        draw_view(screen, game_state)
        pygame.display.update()
        clock.tick(60)
        
    if game_state.db_connection:
        game_state.db_connection.close()
    pygame.quit()
    

            

if __name__ == "__main__":
    main()
