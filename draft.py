import pygame
import cv2
import mediapipe as mp
import os


# Getting mediapipe: Hands ready
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Capture webcam
cam = cv2.VideoCapture(0)

# Prepare pygame window position, fonts and background music
os.environ['SDL_VIDEO_WINDOW_POS'] = "200,0"

pygame.font.init()

# Global variables


# s_width = 1200
# s_height = 800

screen = pygame.display.set_mode((s_width, s_height))
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Window name')

# s_width, s_height = screen.get_size()

# print(s_height, s_width)

# put a text in the middle of the screen


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("britannic", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (s_width / 2, s_height / 2))


# draw the main window
def draw_window(surface, reps=0):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('britannic', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))

    surface.blit(label, (s_width / 2 + 200, 15))

    # show current reps
    font = pygame.font.SysFont('britannic', 30)
    label = font.render('reps: ' + str(reps), 1, (255, 255, 255))

    sx = s_width / 2 + 50
    sy = s_height / 2 - 100

    surface.blit(label, (sx + 20, sy + 160))

    pygame.draw.rect(surface, (215, 215, 215), (top_left_x,
                     top_left_y, play_width, play_height), 5)


# THE MAIN FUNCTION THAT RUNS THE GAME
def main(screen):

    reps = 0
    run = True
    num = 0

    # THE MAIN WHILE LOOP
    while run:

        # Set up the hand tracker
        success, img = cam.read()
        imgg = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(imgg, cv2.COLOR_BGR2RGB)

        cv2.namedWindow("WebCam")
        cv2.moveWindow("WebCam", 20, 121)
        cv2.imshow("WebCam", imgg)
        cv2.waitKey(1)

        draw_window(screen, reps)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

    cam.release()
    # cv2.destroyAllwindows()
    pygame.display.quit()


# Menu screen that will lead to the main function


def main_menu(screen):
    run = True
    while run:
        screen.fill((0, 0, 0))
        draw_text_middle(screen, 'Press Any Key To Start', 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(screen)

    pygame.display.quit()


main_menu(screen)
