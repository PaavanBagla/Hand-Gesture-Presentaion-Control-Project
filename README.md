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

👉 1-finger swipe right → Next Slide

👈 1-finger swipe left → Previous Slide

🫵 Index finger Point → Spotlight pointer

🤏 Pinch Out (Index+Middle+Thumb) → Zoom in 

🤏 Pinch In (Index+Middle+Thumb) → Zoom out

✌️ Two-finger drag - Pan Screen

# Acknowledgements
This project is based on [kinivi/hand-gesture-recognition-mediapipe](https://github.com/kinivi/hand-gesture-recognition-mediapipe), which provides the core hand tracking and gesture classification logic using MediaPipe.

I have customized and extended this project for real-time presentation control with additional gesture features.
