from pygame.locals import *
import pygame
import sys


# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((1920, 1080), 0, 32)

font = pygame.font.SysFont(None, 80)
font_levels = pygame.font.SysFont(None, 120)
font_Game_name = pygame.font.SysFont(None, 170)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


click = False


def main_menu():
    while True:
        mx, my = pygame.mouse.get_pos()

        screen.fill((100, 100, 207))
        draw_text('Text Text!', font_Game_name,
                  (0, 0, 0), screen, 600, 200)

        game_button = pygame.Rect(660, 360, 300, 90)
        leaderboard_button = pygame.Rect(660, 500, 400, 90)
        exit_button = pygame.Rect(660, 640, 300, 90)

        pygame.draw.rect(screen, (245, 163, 69), game_button)
        draw_text('Start', font, (0, 0, 0), screen, 680, 380)

        pygame.draw.rect(screen, (245, 163, 69), leaderboard_button)
        draw_text('Leaderboard', font, (0, 0, 0), screen, 680, 520)

        pygame.draw.rect(screen, (245, 163, 69), exit_button)
        draw_text('Quit', font, (0, 0, 0), screen, 680, 660)

        if game_button.collidepoint((mx, my)):
            if click:
                game()
        if leaderboard_button.collidepoint((mx, my)):
            if click:
                leaderboard()
        if exit_button.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        click = False
        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


main_menu()
