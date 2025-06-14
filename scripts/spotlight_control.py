import cv2
import numpy as np
import pyautogui
import time
import subprocess
import platform
import re

class SpotlightController:
    def __init__(self):
        self.overlay_window_name = "Spotlight"
        self.enabled = False
        self.screenshot = None
        self.spotlight_radius = 200
        self.last_update_time = 0
        self.update_cooldown = 1.0
        self.original_window_info = None
        self.is_mac = platform.system() == 'Darwin'

    def take_screenshot(self):
        """Capture the current screen and store it"""
        try:
            if self.is_mac:
                # Get active window info using AppleScript
                script = """
                tell application "System Events"
                    set frontApp to first application process whose frontmost is true
                    set frontAppName to name of frontApp
                    try
                        tell process frontAppName
                            set windowName to name of first window
                        end tell
                        return frontAppName & "|||" & windowName
                    on error
                        return frontAppName
                    end try
                end tell
                """
                result = subprocess.run(['osascript', '-e', script], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    output = result.stdout.strip()
                    if "|||" in output:
                        app_name, window_name = output.split("|||")
                        self.original_window_info = (app_name, window_name)
                        print(f"Original window: {app_name} - {window_name}")
                    else:
                        self.original_window_info = (output, None)
                        print(f"Original app: {output} (no window name)")
                else:
                    print("Couldn't get active window info")
                    self.original_window_info = None
            else:
                # Windows/Linux implementation would go here
                self.original_window_info = None
        except Exception as e:
            print(f"Couldn't get active window: {e}")
            self.original_window_info = None

        screen = pyautogui.screenshot()
        screen_width, screen_height = pyautogui.size()
        screen = screen.resize((screen_width, screen_height))
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
        
        base = self.screenshot.copy()
        h, w, _ = base.shape

        # Create dark overlay
        dark_overlay = base.copy()
        dark_overlay[:] = (0, 0, 0)
        alpha = 0.3

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
        cv2.setWindowProperty(self.overlay_window_name, cv2.WND_PROP_TOPMOST, 1)
        self.enabled = True

    def hide_spotlight(self):
        """Hide the spotlight overlay and restore original window"""
        if self.enabled:
            cv2.destroyWindow(self.overlay_window_name)
            self.enabled = False
            self.screenshot = None
            
            # Restore the original window after a small delay
            time.sleep(0.3)
            
            if self.is_mac and self.original_window_info:
                try:
                    app_name, window_name = self.original_window_info
                    if window_name:
                        # Try to activate specific window
                        script = f"""
                        tell application "{app_name}"
                            activate
                            try
                                set targetWindow to window "{window_name}"
                                set index of targetWindow to 1
                            on error
                                -- If window not found, just activate app
                                activate
                            end try
                        end tell
                        """
                    else:
                        # Just activate the app if we don't have window name
                        script = f'tell application "{app_name}" to activate'
                    
                    subprocess.run(['osascript', '-e', script])
                    print(f"Restored focus to: {app_name}" + 
                         (f" - {window_name}" if window_name else ""))
                except Exception as e:
                    print(f"Couldn't restore window focus: {e}")
            else:
                print("No original window to restore or not on macOS")