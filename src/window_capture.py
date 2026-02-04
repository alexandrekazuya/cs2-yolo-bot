"""
Window capture utilities for CS2 Bot
Handles window detection and screen capture
"""

import numpy as np
import win32gui
import win32ui
import ctypes


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
    """Capture a specific window by handle."""
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    width = right - left
    height = bottom - top
    
    if width == 0 or height == 0:
        return None, 0, 0
    
    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()
    
    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(bitmap)
    
    ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 3)
    
    bmp_info = bitmap.GetInfo()
    bmp_str = bitmap.GetBitmapBits(True)
    frame = np.frombuffer(bmp_str, dtype=np.uint8)
    frame = frame.reshape((bmp_info['bmHeight'], bmp_info['bmWidth'], 4))
    
    # Cleanup
    try:
        win32gui.DeleteObject(bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
    except Exception:
        pass
    finally:
        win32gui.ReleaseDC(hwnd, hwnd_dc)
    
    import cv2
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    
    return frame, width, height


def is_game_focused(window_title: str) -> bool:
    """Check if the game window is currently focused."""
    try:
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        return window_title.lower() in title.lower()
    except:
        return False
