import pyautogui
import time

class MoveController:
    def __init__(self):
        self.prev_point = None
        self.last_move_time = 0
        self.cooldown = 0.01  # seconds between moves (very low)
        self.sensitivity = 1.5  # scale the movement (tune this)

    def move_cursor(self, current_point):
        """
        Move mouse relative to finger motion.
        current_point: [x, y] coordinates of fingertip (e.g., index finger)
        """
        current_time = time.time()
        if self.prev_point is None:
            self.prev_point = current_point
            return

        if current_time - self.last_move_time < self.cooldown:
            return

        dx = (current_point[0] - self.prev_point[0]) * self.sensitivity
        dy = (current_point[1] - self.prev_point[1]) * self.sensitivity

        pyautogui.moveRel(dx, dy)
        self.prev_point = current_point
        self.last_move_time = current_time

    def reset(self):
        """Reset previous point when gesture ends or hand is lost"""
        self.prev_point = None
