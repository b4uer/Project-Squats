import pygame
import sys

from sample_menu import Menu


# Initialize
pygame.init()

# Create Window/Display
WINDOW_NAME = "Window"
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(WINDOW_NAME)

# Initialize Clock for FPS
FPS = 30
clock = pygame.time.Clock()

# Variables ------------------------------------------------------- #
global state
state = "game"


# game = Game(window)
menu = Menu(SCREEN)

# Functions


def user_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


def update():

    menu.main_menu()
    # game.update()

    pygame.display.update()
    clock.tick(FPS)


# Main loop
while True:

    # Events
    user_events()

    # Update
    update()
