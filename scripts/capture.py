"""
Screenshot Capture Utility for Dataset Collection
Press 'c' to capture, 'q' to quit
"""

import cv2
import mss
import numpy as np
import os
from datetime import datetime
import keyboard  # pip install keyboard


def capture_screenshots(
    output_dir: str = "captures",
    capture_key: str = "c",
    quit_key: str = "q",
):
    """
    Capture screenshots for dataset collection.
    
    Args:
        output_dir: Directory to save screenshots
        capture_key: Key to press for capturing
        quit_key: Key to press to quit
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 50)
    print("Screenshot Capture Utility")
    print("=" * 50)
    print(f"Output directory: {output_dir}")
    print(f"Press '{capture_key}' to capture a screenshot")
    print(f"Press '{quit_key}' to quit")
    print("=" * 50)
    
    capture_count = 0
    
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor
        
        while True:
            # Check for capture key
            if keyboard.is_pressed(capture_key):
                # Capture screenshot
                screenshot = sct.grab(monitor)
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                
                # Generate filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                filename = f"cs2_{timestamp}.jpg"
                filepath = os.path.join(output_dir, filename)
                
                # Save image
                cv2.imwrite(filepath, frame)
                capture_count += 1
                print(f"[{capture_count}] Saved: {filename}")
                
                # Small delay to prevent multiple captures from single press
                cv2.waitKey(200)
            
            # Check for quit key
            if keyboard.is_pressed(quit_key):
                break
            
            # Small delay to reduce CPU usage
            cv2.waitKey(10)
    
    print("\n" + "=" * 50)
    print(f"Capture complete! Saved {capture_count} screenshots to '{output_dir}'")
    print("=" * 50)


if __name__ == "__main__":
    capture_screenshots()
