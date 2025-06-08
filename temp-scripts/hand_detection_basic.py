###### What does this script does:
    # Access the webcam
    # Use MediaPipe Hands to detect a hand
    # Draw hand landmarks on the video feed
    # Display the FPS

import cv2 # → OpenCV for webcam access and display
import mediapipe as mp # → MediaPipe for hand detection and landmarks
import pyautogui
import numpy as np

pyautogui.FAILSAFE = False  # Disable fail-safe for smooth control

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(1)

screen_w, screen_h = pyautogui.size()
finger_tips_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

# Configure Mediapipe Hands
with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7) as hands:
    while cap.isOpened(): # Loop while webcam is open
        success, frame = cap.read()
        if not success:
            break

        # Flip the frame horizontally (mirror-image) and convert the color
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame and detect hands
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get all landmarks positions
                lm_list = []
                h, w, _ = frame.shape
                for id, lm in enumerate(hand_landmarks.landmark):
                    lm_list.append((id, int(lm.x * w), int(lm.y * h)))
                
                fingers = []
                # Thumb (check x difference for left/right)
                if lm_list[4][1] > lm_list[3][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                
                # Other 4 fingers (check y)
                for tip_id in [8, 12, 16, 20]:
                    if lm_list[tip_id][2] < lm_list[tip_id - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                # print(f"Fingers up: {fingers}")  # e.g., [1, 1, 0, 0, 0] => thumb and index up

                # Control mouse only if index finger is up
                if fingers == [0,1,0,0,0]:  # Only index finger up
                    x, y = lm_list[8][1], lm_list[8][2] # Index Tip Coords

                    # Convert to screen coordinates
                    screen_x = np.interp(x, [0, w], [0, screen_w])
                    screen_y = np.interp(y, [0, h], [0, screen_h])

                    pyautogui.moveTo(screen_x, screen_y)

                # Next slide: index + middle fingers up
                elif fingers == [0, 1, 1, 0, 0]:
                    pyautogui.press('right')

                # Left click: fist (no fingers)
                elif fingers == [0, 0, 0, 0, 0]:
                    pyautogui.click()

                # Zoom in: thumb + index
                elif fingers == [1, 1, 0, 0, 0]:
                    pyautogui.hotkey('ctrl', '+')

                # Zoom out: thumb + pinky
                elif fingers == [1, 0, 0, 0, 1]:
                    pyautogui.hotkey('ctrl', '-')

                # Draw landmarks and connections
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Display the output
        cv2.imshow('Gesture Control', frame)

        # Exit with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Clean up
cap.release()
cv2.destroyAllWindows()




