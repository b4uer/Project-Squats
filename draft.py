import pygame
import cv2
import mediapipe as mp
import os


pygame.init()

# Global variables
# s_width = 1200
# s_height = 800

# screen = pygame.display.set_mode((s_width, s_height))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Window name')

# s_width, s_height = screen.get_size()
s_width = screen.get_width()
s_height = screen.get_height()
print(s_width, s_height)


def draw_feedback(surface):
    surface.fill((50, 0, 100))

    pygame.font.init()
    font = pygame.font.SysFont('britannic', 60)
    label = font.render('Feedback', 1, (255, 255, 255))
    surface.blit(label, (s_width / 2 - 30, s_height / 2 - 420))

    # create a surface object, image is drawn on it.
    imp = pygame.image.load("Feedback.png").convert()

    # Using blit to copy content from one surface to other
    screen.blit(imp, (s_width / 2 - 400, s_height / 2 - 330))

    img_check = pygame.image.load("GreenCheck.png").convert_alpha()
    img_cross = pygame.image.load("RedCross.png").convert_alpha()

    screen.blit(img_check, (s_width / 2 - 500, s_height / 2 - 320))
    screen.blit(img_check, (s_width / 2 - 500, s_height / 2 - 170))
    screen.blit(img_check, (s_width / 2 - 500, s_height / 2))
    screen.blit(img_check, (s_width / 2 - 500, s_height / 2 + 160))
    screen.blit(img_check, (s_width / 2 - 500, s_height / 2 + 300))

    # display
    pygame.display.update()


def main(screen):
    run = True
    while run:
        draw_feedback(screen)
        # pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    break


main(screen)
