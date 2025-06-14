import cv2
import numpy as np
import mss
import pyautogui
import time


class SpotlightController:
    def __init__(self):
        self.overlay_window_name = "Spotlight"
        self.enabled = False
        self.screenshot = None
        self.spotlight_radius = 200  # Adjust size here
        self.last_update_time = 0
        self.update_cooldown = 1.0  # seconds between allowed screenshot updates

    def take_screenshot(self):
        """Capture the current screen and store it"""
        screen = pyautogui.screenshot()
        screen_width, screen_height = pyautogui.size()
        screen = screen.resize((screen_width, screen_height))  # Ensure exact size
        self.screenshot = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
        self.last_update_time = time.time()

    def refresh_screenshot(self):
        """Force a screenshot refresh if cooldown has passed"""
        current_time = time.time()
        if current_time - self.last_update_time > self.update_cooldown:
            self.take_screenshot()
            return True
        return False

    def show_spotlight(self, finger_pos, force_refresh=False):
        """Show spotlight at finger position"""
        if force_refresh or self.screenshot is None:
            self.take_screenshot()
        
        # Make a copy of the screenshot
        base = self.screenshot.copy()
        h, w, _ = base.shape

        # Create dark overlay
        dark_overlay = base.copy()
        dark_overlay[:] = (0, 0, 0)
        alpha = 0.3  # 70% dark

        # Create circular mask
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask, finger_pos, self.spotlight_radius, 255, -1)
        mask_3d = cv2.merge([mask] * 3)

        # Blend only non-spotlight regions
        inv_mask = cv2.bitwise_not(mask_3d)
        darkened = cv2.addWeighted(base, alpha, dark_overlay, 1 - alpha, 0)
        spotlight = cv2.bitwise_and(base, mask_3d)
        dimmed = cv2.bitwise_and(darkened, inv_mask)
        final = cv2.add(spotlight, dimmed)

        cv2.namedWindow(self.overlay_window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(self.overlay_window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(self.overlay_window_name, final)
        cv2.setWindowProperty(self.overlay_window_name, cv2.WND_PROP_TOPMOST, 1)  # Keep on top
        self.enabled = True

    def hide_spotlight(self):
        """Hide the spotlight overlay"""
        if self.enabled:
            cv2.destroyWindow(self.overlay_window_name)
            self.enabled = False
            self.screenshot = None  # Clear screenshot to force refresh next time