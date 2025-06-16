# Hand Gesture Controller for Presentations
Control the Google Presentation slides with Hand Gesture

# Installation
**Step 1: Create and activate the conda environment**
```bash
conda create -n hand_gesture_env python=3.9 -y
conda activate hand_gesture_env
```
**Step 2: Clone GithubRepo**
```bash
git clone https://github.com/PaavanBagla/Hand-Gesture-Presentaion-Control-Project.git
```
**Step 3: Install Dependencies**
```bash
pip3 install mediapipe opencv-python pyautogui tensorflow
```
OR
```bash
pip install mediapipe opencv-python pyautogui tensorflow
```
Total Space needed for conda environment: 3.2 GB

# Usage
Run the app with:
```bash
python3 app.py
```
You can also pass optional arguments to customize camera and detection settings:
```bash
python3 app.py --device 0 --width 1280 --height 720 --min_detection_confidence 0.8 --min_tracking_confidence 0.6
```

### Available Arguments
- `--device`: Camera device ID (default: `1`)
- `--width` / `--height`: Capture resolution (default: `960x540`)
- `--use_static_image_mode`: Enable static image mode
- `--min_detection_confidence`: Detection threshold (default: `0.7`)
- `--min_tracking_confidence`: Tracking threshold (default: `0.5`)
  
### To exit the app
- Press the **ESC** key while the camera window is open
# Goal
Control Google Slides via:

👉 3-fingers swipe left → Next Slide

👈 3-fingers swipe right → Previous Slide

🫵 Index finger Point → Spotlight pointer

🤏 Pinch Out (Index+Middle+Thumb) → Zoom in 

🤏 Pinch In (Index+Middle+Thumb) → Zoom out

✌️ Two-finger drag → Pan Screen

# Swipe + Spotlight Control Feature
https://github.com/user-attachments/assets/248864cf-e204-47c5-91fc-a92e8f07b8e3
# Acknowledgements
This project is based on [kinivi/hand-gesture-recognition-mediapipe](https://github.com/kinivi/hand-gesture-recognition-mediapipe), which provides the core hand tracking and gesture classification logic using MediaPipe.

I have customized and extended this project for real-time presentation control with additional gesture features.
