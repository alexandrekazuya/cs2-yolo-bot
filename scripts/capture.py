import cv2
import numpy as np
import os
import sys
from datetime import datetime
import keyboard  # pip install keyboard
import time

# Add project root to path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.window_capture import find_window, capture_window, is_game_focused
from src.config import WINDOW_TITLE


def capture_screenshots(
    output_dir: str = "captures",
    capture_key: str = "c",
    quit_key: str = "q",
    window_title: str = WINDOW_TITLE
):

    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 50)
    print("Screenshot Capture Utility (Window-Specific)")
    print("=" * 50)
    print(f"Target Window: {window_title}")
    print(f"Output directory: {output_dir}")
    print(f"Press '{capture_key}' to capture a screenshot")
    print(f"Press '{quit_key}' to quit")
    print("=" * 50)
    
    # Find game window
    windows = find_window(window_title)
    if not windows:
        print(f"ERROR: Window '{window_title}' not found!")
        print("Please make sure the game is running.")
        return
    
    target_hwnd, found_title = windows[0]
    print(f"Found window: {found_title}")
    
    capture_count = 0
    
    while True:
        # Check for capture key
        if keyboard.is_pressed(capture_key):
            # Check if game window is focused (highly recommended for clean data)
            if not is_game_focused(window_title):
                print("Warning: Game window not focused. Skipping capture.")
                time.sleep(0.5)
                continue

            # Capture window
            frame, width, height = capture_window(target_hwnd)
            
            if frame is None:
                print("ERROR: Could not capture window! Is it minimized?")
                time.sleep(1)
                continue
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"cs2_{timestamp}.jpg"
            filepath = os.path.join(output_dir, filename)
            
            # Save image
            cv2.imwrite(filepath, frame)
            capture_count += 1
            print(f"[{capture_count}] Saved: {filename} ({width}x{height})")
            
            # Small delay to prevent multiple captures from single press
            time.sleep(0.3)
        
        # Check for quit key
        if keyboard.is_pressed(quit_key):
            break
        
        # Small delay to reduce CPU usage
        time.sleep(0.01)
    
    print("\n" + "=" * 50)
    print(f"Capture complete! Saved {capture_count} screenshots to '{output_dir}'")
    print("=" * 50)


if __name__ == "__main__":
    capture_screenshots()
