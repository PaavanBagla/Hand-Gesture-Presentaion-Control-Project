# Hand Gesture Controller for Presentations
Control the Google Presentation slides with Hand Gesture

# Installation
**Step 1: Create and activate the conda environment**
```bash
conda create -n hand_gesture_env python=3.9 -y
conda activate hand_gesture_env
```
**Step 2: Install Dependencies**
```bash
pip3 install mediapipe opencv-python pyautogui
```

# Goal
Control Google Slides via:

👉 Three fingers or 1 finger (whichever is better) swipe left → Next Slide

👈 Three fingers or 1 finger (whichever is better) swipe right  → Previous Slide

🫵 Index finger Point →  should Spot light the the pointed area on the slide 

🤏 Index Finger + Middle Finger + Thumb pinch out → Zoom in 

🤏 Index Finger + Middle Finger + Thumb pinch in → Zoom out

✌️ Index Finger + Middle finger movement should behave like i HAVE TOUCH SCREEN CONTROL to move (if zoomed in)

# Acknowledgements
This project is based on [kinivi/hand-gesture-recognition-mediapipe](https://github.com/kinivi/hand-gesture-recognition-mediapipe), which provides the core hand tracking and gesture classification logic using MediaPipe.

I have customized and extended this project for real-time presentation control with additional gesture features.
