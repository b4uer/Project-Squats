import pygame
import sys


from pygame.locals import *


class Menu(object):
    def __init__(self, surface):
        self.font = pygame.font.SysFont(None, 80)
        self.font_levels = pygame.font.SysFont(None, 120)
        self.font_Game_name = pygame.font.SysFont(None, 170)
        self.screen = surface

    def draw_text(text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    click = False

    def main_menu(self):
        while True:
            mx, my = pygame.mouse.get_pos()

            self.screen.fill((150, 87, 217))
            self.draw_text('Tex Text!', self.font_Game_name,
                           (0, 0, 0), self.screen, 600, 70)
            game_button = pygame.Rect(860, 300, 300, 90)
            leaderboard_button = pygame.Rect(300, 550, 400, 90)
            exit_button = pygame.Rect(1400, 550, 300, 90)
            if game_button.collidepoint((mx, my)):
                if click:
                    # self.game()
                    print("game")
            if leaderboard_button.collidepoint((mx, my)):
                if click:
                    # self.leaderboard()
                    print("leaderboard")
            if exit_button.collidepoint((mx, my)):
                if click:
                    pygame.quit()
                    sys.exit()

            pygame.draw.rect(self.screen, (245, 163, 69), game_button)
            self.draw_text('Start', font, (0, 0, 0), self.screen, 945, 320)
            pygame.draw.rect(self.screen, (245, 163, 69), leaderboard_button)
            draw_text('Leaderboard', font, (0, 0, 0), self.screen, 320, 570)
            pygame.draw.rect(self.screen, (245, 163, 69), exit_button)
            self.draw_text('Quit', font, (0, 0, 0), self.screen, 1485, 570)
            click = False

            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            # pygame.display.update()
            # mainClock.tick(60)
