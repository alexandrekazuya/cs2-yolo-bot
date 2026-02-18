"""
Window capture utilities for CS2 Bot
Uses mss for fast BitBlt-based screen capture
"""

import numpy as np
import cv2
import win32gui
import mss

# Reusable mss instance
_sct = mss.mss()


def find_window(window_title: str):
    """Find a window by partial title match."""
    result = []
    
    def enum_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if window_title.lower() in title.lower():
                result.append((hwnd, title))
    
    win32gui.EnumWindows(enum_callback, None)
    return result


def capture_window(hwnd):
    """Capture a specific window by handle using mss."""
    try:
        rect = win32gui.GetClientRect(hwnd)
        point = win32gui.ClientToScreen(hwnd, (rect[0], rect[1]))
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        
        if width == 0 or height == 0:
            return None, 0, 0
        
        left, top = point
        monitor = {"left": left, "top": top, "width": width, "height": height}
        
        frame = np.array(_sct.grab(monitor))
        # mss returns BGRA, convert to BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        
        return frame, width, height
    except Exception:
        return None, 0, 0


def cleanup_camera():
    """Close the mss instance."""
    try:
        _sct.close()
    except Exception:
        pass


def is_game_focused(window_title: str) -> bool:
    """Check if the game window is currently focused."""
    try:
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        return window_title.lower() in title.lower()
    except:
        return False
