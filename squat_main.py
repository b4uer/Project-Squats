import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


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


print("test test")
cap = cv2.VideoCapture(1)

# Curl counter variables
counter = 0
knee_mistake = 0
stage = None

# Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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

            # print(round(shoulder[1], 2), round(other_shoulder[1], 2))

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
            angle_abs = abs(knee_angle - hip_angle)
            # Visualize angle
            cv2.putText(image, str(knee_angle),
                        tuple(np.multiply(knee,
                              [640, 480]).astype(int)),
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
            if knee_angle > 150:
                stage = "up"
            if knee_angle < 90 and stage == "up":
                stage = "down"
                counter += 1

            if knee_angle < 40 and stage == "up":
                knee_mistake += 1
            print(knee_mistake)
            # print(angle_abs)
            # if abs(knee_angle - hip_angle) > 30:
            #     print("BAD!!!!!!")

            # print(abs(shoulder[1] - other_shoulder[1])*100)
            # if abs(shoulder[1] - other_shoulder[1]) > 10:
            #     print("BAD!!!!!!")

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

        cv2.imshow('Mediapipe Feed', image)  # cv2.flip(image, 1)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        if cv2.waitKey(10) & 0xFF == ord('r'):
            counter = 0

    cap.release()
    cv2.destroyAllWindows()
