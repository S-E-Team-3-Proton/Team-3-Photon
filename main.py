import pygame
from game import init_game, GameState, draw_entry_screen, handle_event

def main():

    pygame.init()
    pygame.font.init()

    init_game()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 650
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Laser Tag Game")

    photon_logo = pygame.image.load("logo.jpg")
    photon_logo = pygame.transform.scale(photon_logo, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(photon_logo, (0, 0))
    pygame.display.update()
    pygame.time.wait(3000)  # Display splash screen for 3 seconds
    
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
    main()

            

if __name__ == "__main__":
    main()
