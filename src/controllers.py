"""
Controller classes for CS2 Bot
Handles movement, aiming, shooting, and hotkey listening
"""

import time
import threading
import pydirectinput
import win32api
import win32con
from pynput import keyboard
from src.config import MOVE_KEYS, MOVE_INTERVAL, AIM_SPEED, TOGGLE_HOTKEY

# Disable pydirectinput pause between actions
pydirectinput.PAUSE = 0


class HotkeyListener:
    """Global hotkey listener to toggle bot on/off."""
    
    def __init__(self, toggle_callback):
        self.toggle_callback = toggle_callback
        self.listener = None
    
    def start(self):
        """Start listening for hotkeys."""
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()
    
    def stop(self):
        """Stop listening."""
        if self.listener:
            self.listener.stop()
    
    def _on_press(self, key):
        """Handle key press."""
        if key == TOGGLE_HOTKEY:
            self.toggle_callback()


class MovementController:
    """Handles A/D strafing movement."""
    
    def __init__(self):
        self.running = False
        self.paused = False
        self.current_key = None
        self.thread = None
    
    def start(self):
        self.running = True
        self.paused = False
        self.thread = threading.Thread(target=self._movement_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        self.running = False
        if self.current_key:
            pydirectinput.keyUp(self.current_key)
            self.current_key = None
    
    def _movement_loop(self):
        key_index = 0
        while self.running:
            if self.paused:
                if self.current_key:
                    pydirectinput.keyUp(self.current_key)
                    self.current_key = None
                time.sleep(0.01)
                continue

            # Release previous key
            if self.current_key:
                pydirectinput.keyUp(self.current_key)
            
            # Press new key
            self.current_key = MOVE_KEYS[key_index]
            pydirectinput.keyDown(self.current_key)
            
            # Alternate direction
            key_index = (key_index + 1) % len(MOVE_KEYS)
            
            # Wait for interval, but check for pause/stop frequently
            elapsed = 0
            while elapsed < MOVE_INTERVAL and self.running and not self.paused:
                time.sleep(0.05)
                elapsed += 0.05
    
    def pause(self):
        """Pause movement temporarily."""
        self.paused = True
        if self.current_key:
            pydirectinput.keyUp(self.current_key)
            self.current_key = None
    
    def resume(self):
        """Resume movement."""
        self.paused = False


class AimController:
    """Handles aiming and shooting."""
    
    def __init__(self, screen_width, screen_height):
        self.screen_center_x = screen_width // 2
        self.screen_center_y = screen_height // 2
    
    def aim_at_target(self, target_x, target_y):
        """Move mouse to aim at target position."""
        # Calculate offset from screen center
        offset_x = int((target_x - self.screen_center_x) * AIM_SPEED)
        offset_y = int((target_y - self.screen_center_y) * AIM_SPEED)
        
        # Move mouse relative to current position
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, offset_x, offset_y, 0, 0)
    
    def shoot(self):
        """Perform a single click to shoot."""
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
