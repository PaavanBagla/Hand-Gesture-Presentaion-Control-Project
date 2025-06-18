import cv2
import numpy as np
import pyautogui
import time
import subprocess
import platform
import sys

class SpotlightController:
    def __init__(self):
        self.overlay_window_name = "Spotlight"
        self.enabled = False
        self.screenshot = None
        self.spotlight_radius = 200
        self.last_update_time = 0
        self.update_cooldown = 1.0
        self.original_window_info = None
        self.os_type = platform.system()
        
        # Print OS information
        os_info = {
            'Darwin': 'macOS',
            'Windows': 'Windows',
            'Linux': 'Linux'
        }.get(self.os_type, self.os_type)
        print("----")
        print(f"🖥️ Operating System: {os_info}")
        
        # Platform-specific initialization
        if self.os_type == 'Darwin':  # macOS
            print("🔧 Using macOS window management")
            print("----")
            self.get_window_info = self._get_mac_window_info
            self.restore_window = self._restore_mac_window
        elif self.os_type == 'Windows':
            print("🔧 Using Windows window management")
            print("----")
            self.get_window_info = self._get_win_window_info
            self.restore_window = self._restore_win_window
        else:  # Linux/other
            print("🔧 Using Linux/other window management")
            print("----")
            self.get_window_info = self._get_linux_window_info
            self.restore_window = self._restore_linux_window
    
    def _get_mac_window_info(self):
        """Get active window info on macOS"""
        try:
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
                    return output.split("|||")
                return (output, None)
        except Exception as e:
            print(f"Couldn't get macOS window info: {e}")
        return (None, None)

    def _get_win_window_info(self):
        """Get active window info on Windows"""
        try:
            import win32gui
            window = win32gui.GetForegroundWindow()
            title = win32gui.GetWindowText(window)
            exe_name = None
            
            # Try to get the executable name
            try:
                import psutil
                pid = win32gui.GetWindowThreadProcessId(window)[1]
                exe_name = psutil.Process(pid).name()
            except:
                pass
                
            return (exe_name or "unknown", title or "unknown")
        except Exception as e:
            print(f"Couldn't get Windows window info: {e}")
        return (None, None)

    def _get_linux_window_info(self):
        """Get active window info on Linux"""
        try:
            # Try using xdotool if available
            try:
                id_result = subprocess.run(['xdotool', 'getactivewindow'], 
                                        capture_output=True, text=True)
                if id_result.returncode == 0:
                    window_id = id_result.stdout.strip()
                    name_result = subprocess.run(['xdotool', 'getwindowname', window_id],
                                                capture_output=True, text=True)
                    if name_result.returncode == 0:
                        return ("unknown", name_result.stdout.strip())
            except:
                pass
        except Exception as e:
            print(f"Couldn't get Linux window info: {e}")
        return (None, None)

    def _restore_mac_window(self, app_name, window_name):
        """Restore window on macOS"""
        try:
            if window_name:
                script = f"""
                tell application "{app_name}"
                    activate
                    try
                        set targetWindow to window "{window_name}"
                        set index of targetWindow to 1
                    on error
                        activate
                    end try
                end tell
                """
            else:
                script = f'tell application "{app_name}" to activate'
            
            subprocess.run(['osascript', '-e', script])
            return True
        except Exception as e:
            print(f"Couldn't restore macOS window: {e}")
        return False

    def _restore_win_window(self, app_name, window_title):
        """Restore window on Windows"""
        try:
            import win32gui
            import win32con
            
            def callback(hwnd, extra):
                if window_title.lower() in win32gui.GetWindowText(hwnd).lower():
                    extra.append(hwnd)
                return True
                
            windows = []
            win32gui.EnumWindows(callback, windows)
            
            if windows:
                hwnd = windows[0]
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(hwnd)

                # Small delay to ensure window is focused
                time.sleep(0.5)
                
                return True
        except Exception as e:
            print(f"Couldn't restore Windows window: {e}")
        return False

    def _restore_linux_window(self, app_name, window_title):
        """Restore window on Linux"""
        try:
            # Try using wmctrl if available
            try:
                subprocess.run(['wmctrl', '-a', window_title])
                return True
            except:
                pass
        except Exception as e:
            print(f"Couldn't restore Linux window: {e}")
        return False

    def take_screenshot(self):
        """Capture the current screen and store it"""
        try:
            self.original_window_info = self.get_window_info()
            if self.original_window_info[0]:
                print(f"Original window: {self.original_window_info[0]} - {self.original_window_info[1] or ''}")
            else:
                print("Couldn't get window info")
        except Exception as e:
            print(f"Couldn't get active window: {e}")
            self.original_window_info = (None, None)

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

            if self.original_window_info and self.original_window_info[0]:
                app_name, window_name = self.original_window_info
                success = self.restore_window(app_name, window_name)
                if success:
                    print(f"Restored focus to: {app_name}" + 
                        (f" - {window_name}" if window_name else ""))

                    # Give some time for window to properly regain focus
                    time.sleep(0.5)

                    # # Optional: simulate click to help focus
                    # screen_width, screen_height = pyautogui.size()
                    # pyautogui.click(screen_width // 2, screen_height // 2)
                else:
                    print("Failed to restore window focus")
            else:
                print("No original window to restore")