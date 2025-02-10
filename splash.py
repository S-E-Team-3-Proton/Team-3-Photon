import pygame
import time

pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Code for how long screen stays on in miliseconds
SPLASH_TIMER = 6000 # 6 seconds

# Loading the splash screen logo
photon_logo = pygame.image.load("logo.jpg")
photon_logo = pygame.transform.scale(photon_logo, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Displaying splash screen logo
screen.blit(photon_logo, (0, 0))
pygame.display.update()

# Wait for splash duration
start_time = pygame.time.get_ticks()

splash_running = True
while splash_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Check if the splash duration has passed
    if pygame.time.get_ticks() - start_time > SPLASH_TIMER:
        splash_running = False

# Splash Screen Disappear Transition
screen.fill((0, 0, 0))  
pygame.display.update()


# Main game code
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Future code goes under here
    
    pygame.display.update()

pygame.quit()