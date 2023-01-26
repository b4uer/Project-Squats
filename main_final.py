import pygame
import cv2
import mediapipe as mp
import numpy as np
import os
import sys

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Capture webcam
cam = cv2.VideoCapture(1)

# Prepare pygame window position, fonts and background music
# os.environ['SDL_VIDEO_WINDOW_POS'] = "200,0"

pygame.init()

# Global variables
neck_check = True
shoulder_check = True
hips_check = True
knee_check = True
ankle_check = True
knee_bended = True

# screen = pygame.display.set_mode((s_width, s_height))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Window name')

# s_width, s_height = screen.get_size()
s_width = screen.get_width()
s_height = screen.get_height()
print(s_width, s_height)

# Curl counter variables
counter = 0
knee_mistake = 0
stage = None
buff_var = 0


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
        np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


# draw the main window
def draw_window(surface, counter=0, knee_mistake=0):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('britannic', 60)
    label = font.render('SquatCam', 1, (255, 255, 255))

    surface.blit(label, (s_width / 2 + 200, s_height / 2 - 420))

    # show current reps
    font = pygame.font.SysFont('britannic', 40)
    label = font.render('reps: ' + str(counter), 1, (255, 255, 255))
    surface.blit(label, (s_width / 2, s_height / 2 - 200))

    # show knee mistakes
    font = pygame.font.SysFont('britannic', 40)
    label = font.render('knee bended too much: ' +
                        str(knee_mistake), 1, (255, 255, 255))
    surface.blit(label, (s_width / 2, s_height / 2 - 100))

    pygame.display.update()


def draw_feedback(surface, knee_mistake, shoulder_check, hips_check):
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

    print(shoulder_check)
    # display green check or red cross
    if neck_check:
        screen.blit(img_check, (s_width / 2 - 500, s_height / 2 - 320))
    else:
        screen.blit(img_cross, (s_width / 2 - 500, s_height / 2 - 320))
    if shoulder_check:
        screen.blit(img_check, (s_width / 2 - 500, s_height / 2 - 170))
    else:
        screen.blit(img_cross, (s_width / 2 - 500, s_height / 2 - 170))
    if hips_check:
        screen.blit(img_check, (s_width / 2 - 500, s_height / 2))
    else:
        screen.blit(img_cross, (s_width / 2 - 500, s_height / 2))
    if knee_mistake < 4:
        screen.blit(img_check, (s_width / 2 - 500, s_height / 2 + 160))
    else:
        screen.blit(img_cross, (s_width / 2 - 500, s_height / 2 + 160))
    if ankle_check:
        screen.blit(img_check, (s_width / 2 - 500, s_height / 2 + 300))
    else:
        screen.blit(img_cross, (s_width / 2 - 500, s_height / 2 + 300))

    # display
    pygame.display.update()


# THE MAIN FUNCTION THAT RUNS THE GAME
def main(screen):

    counter = 0
    knee_mistake = 0

    shoulder_check = True
    hips_check = True
    knee_check = True

    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cam.isOpened():
            ret, frame = cam.read()
            img = cv2.flip(frame, 1)

            # Recolor image to RGB
            image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                hip = [
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y,
                ]
                knee = [
                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y,
                ]
                ankle = [
                    landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y,
                ]
                shoulder = [
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
                ]
                other_shoulder = [
                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
                ]
                elbow = [
                    landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y
                ]
                wrist = [
                    landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y
                ]

                # Calculate angle
                angle = calculate_angle(shoulder, elbow, wrist)

                # Knee joint angle
                knee_angle = calculate_angle(hip, knee, ankle)
                knee_angle = round(knee_angle, 2)

                # Hip joint angle
                hip_angle = calculate_angle(shoulder, hip, knee)
                hip_angle = round(hip_angle, 2)

                # cv2.putText(image, str(angle),
                #             tuple(np.multiply(elbow, [640, 480]).astype(int)),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,
                #                                             255, 255), 2, cv2.LINE_AA
                #             )

                # Visualize angle
                cv2.putText(image, str(knee_angle),
                            tuple(np.multiply(knee, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10,
                                                            245, 37), 2, cv2.LINE_AA
                            )

                # Visualize angle
                cv2.putText(image, str(hip_angle),
                            tuple(np.multiply(hip, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,
                                                            255, 255), 2, cv2.LINE_AA
                            )

                # Curl counter logic
                if knee_angle > 120:
                    stage = "up"
                    knee_check = True
                if knee_angle < 95 and stage == "up":
                    stage = "down"
                    counter += 1

                if knee_angle < 35 and knee_check == True:
                    knee_check = False
                    knee_mistake += 1
                if abs(knee_angle - hip_angle) > 40:
                    hips_check = False
                if abs(shoulder[1] - other_shoulder[1])*100 > 15:
                    shoulder_check = False

                print(shoulder_check)

            except:
                pass

            # Render curl counter
            # Setup status box
            cv2.rectangle(image, (0, 0), (100, 73), (0, 0, 0), -1)

            # Rep data
            cv2.putText(image, 'REPS', (15, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (245, 117, 16), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter),
                        (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # Render detections
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(
                    color=(245, 117, 66), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(
                    color=(245, 66, 230), thickness=2, circle_radius=2)
            )

            cv2.namedWindow("WebCam")
            cv2.moveWindow("WebCam", 20, 121)
            cv2.imshow("WebCam", image)
            cv2.waitKey(1)

            draw_window(screen, counter, knee_mistake)

            if counter == 4:
                cam.release()
                cv2.destroyWindow("WebCam")

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()

    run = True
    while run:
        draw_feedback(screen, knee_mistake, shoulder_check, hips_check)
        # pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    break
        # pygame.quit()


# Menu screen that will lead to the main function
def main_menu(screen):
    # knee_mistake = 0
    run = True
    while run:
        screen.fill((150, 150, 150))

        # create a surface object, image is drawn on it.
        imp = pygame.image.load("firstScreen.jpg").convert()

        # Using blit to copy content from one surface to other
        screen.blit(imp, (0, 0))

        # Drawing Rectangle
        pygame.draw.rect(screen, (100, 240, 240), pygame.Rect(
            s_width / 2 + 20, s_height - 120, s_width, s_height))
        font = pygame.font.SysFont("britannic", 60, bold=True)
        label = font.render('Press Any Key To Start', 1, (0, 0, 0))
        screen.blit(label, (s_width / 2 + 80, s_height - 80))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    break

            if event.type == pygame.KEYDOWN:
                main(screen)

        pygame.display.update()

    # pygame.quit()


main_menu(screen)
