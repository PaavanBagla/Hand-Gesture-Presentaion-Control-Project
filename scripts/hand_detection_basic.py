###### What does thsi script does:
    # Access the webcam
    # Use MediaPipe Hands to detect a hand
    # Draw hand landmarks on the video feed
    # Display the FPS

import cv2 # → OpenCV for webcam access and display
import mediapipe as mp # → MediaPipe for hand detection and landmarks
import time # → Time for FPS calculation

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(1)

# Configure Mediapipe Hands
with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7) as hands:
    prev_time = 0  # Initialize previous time for FPS calculation

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
                # Draw hand landmarks on the frame
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Show FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time else 0
        prev_time = curr_time
        cv2.putText(frame, f'FPS: {int(fps)}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the output
        cv2.imshow('Hand Detection', frame)

        # Exit with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Clean up
cap.release()
cv2.destroyAllWindows()




