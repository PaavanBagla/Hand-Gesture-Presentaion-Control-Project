import time
import pyautogui

class ZoomController:
    def __init__(self):
        self.last_zoom_time = 0
        self.zoom_cooldown = 1.0  # seconds
    
    def zoom(self, direction):
        """Zoom in or out based on direction: 'in' or 'out'"""
        current_time = time.time()
        if current_time - self.last_zoom_time < self.zoom_cooldown:
            return  # Prevent rapid zooming
        
        if direction == "in":
            pyautogui.hotkey('command', '+')
            print("Zoomed In")
        elif direction == "out":
            pyautogui.hotkey('command', '-')
            print("Zoomed Out")
        
        self.last_zoom_time = current_time
