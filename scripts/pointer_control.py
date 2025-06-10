import cv2 as cv
import numpy as np

class SpotlightPointer:
    def __init__(self):
        self.overlay = None
        self.window_name = "Spotlight Overlay"
        cv.namedWindow(self.window_name, cv.WINDOW_NORMAL)
        cv.setWindowProperty(self.window_name, cv.WND_PROP_TOPMOST, 1)
    
    def update_position(self, finger_tip):
        # Create spotlight effect
        overlay = np.zeros((720, 1280, 3), dtype=np.uint8)
        cv.circle(overlay, (finger_tip[0], finger_tip[1]), 
                 50, (255, 255, 255), -1)
        cv.circle(overlay, (finger_tip[0], finger_tip[1]), 
                 50, (0, 0, 0), 2)
        
        # Apply Gaussian blur for spotlight effect
        overlay = cv.GaussianBlur(overlay, (99, 99), 0)
        cv.imshow(self.window_name, overlay)
    
    def hide(self):
        cv.destroyWindow(self.window_name)