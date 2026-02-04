"""
CS2 Real-Time Detection Script
Captures screen and runs YOLOv8 inference in real-time
"""

import cv2
import numpy as np
import mss
import time
from ultralytics import YOLO
import argparse
import win32gui
import win32con
import win32ui
import ctypes


# Screen capture region (adjust for your monitor/game window)
# Set to None to capture entire primary monitor
CAPTURE_REGION = None  # Or: {"top": 0, "left": 0, "width": 1920, "height": 1080}


def get_capture_region(sct):
    """Get the capture region (full primary monitor if not specified)."""
    if CAPTURE_REGION is not None:
        return CAPTURE_REGION
    
    monitor = sct.monitors[1]  # Primary monitor
    return {
        "top": monitor["top"],
        "left": monitor["left"],
        "width": monitor["width"],
        "height": monitor["height"],
    }


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
    # Get window dimensions
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    width = right - left
    height = bottom - top
    
    if width == 0 or height == 0:
        return None
    
    # Get window DC
    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()
    
    # Create bitmap
    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(bitmap)
    
    # Use PrintWindow for better compatibility with games
    ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 3)
    
    # Convert to numpy array
    bmp_info = bitmap.GetInfo()
    bmp_str = bitmap.GetBitmapBits(True)
    frame = np.frombuffer(bmp_str, dtype=np.uint8)
    frame = frame.reshape((bmp_info['bmHeight'], bmp_info['bmWidth'], 4))
    
    # Cleanup
    win32gui.DeleteObject(bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)
    
    # Convert BGRA to BGR
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    
    return frame


def run_detection(
    model_path: str = "runs/detect/cs2_yolov8n/weights/best.pt",
    conf_threshold: float = 0.1,
    show_fps: bool = True,
    show_preview: bool = True,
    window_title: str = None,
):
    """
    Run real-time detection on screen capture.
    
    Args:
        model_path: Path to trained model weights
        conf_threshold: Confidence threshold for detections
        show_fps: Show FPS counter on screen
        show_preview: Show detection preview window
        window_title: Window title to capture (None for full screen)
    """
    # Load the trained model
    print(f"Loading model: {model_path}")
    model = YOLO(model_path)
    
    # Get class names
    class_names = model.names
    print(f"Classes: {class_names}")
    
    # Colors for each class (BGR format)
    colors = {
        0: (0, 0, 255),    # Red for first class
        1: (0, 165, 255),  # Orange for second class
    }
    
    print("\nStarting real-time detection...")
    print("Press 'q' to quit")
    print("-" * 40)
    
    # FPS tracking
    fps_list = []
    
    # Window capture mode
    target_hwnd = None
    if window_title:
        windows = find_window(window_title)
        if windows:
            target_hwnd, found_title = windows[0]
            print(f"Capturing window: {found_title}")
        else:
            print(f"Window '{window_title}' not found. Falling back to full screen.")
    
    with mss.mss() as sct:
        region = get_capture_region(sct)
        if not target_hwnd:
            print(f"Capture region: {region['width']}x{region['height']}")
        
        while True:
            loop_start = time.perf_counter()
            
            # Capture screen or window
            if target_hwnd:
                frame = capture_window(target_hwnd)
                if frame is None:
                    print("Window closed or minimized.")
                    break
            else:
                screenshot = sct.grab(region)
                frame = np.array(screenshot)
                # Convert BGRA to BGR
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            
            # Run inference
            results = model(frame, conf=conf_threshold, verbose=False)
            
            # Process detections
            for result in results:
                boxes = result.boxes
                
                for box in boxes:
                    # Get box coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    # Get class and confidence
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    
                    # Get color and label
                    color = colors.get(cls_id, (0, 255, 0))
                    label = f"{class_names[cls_id]}: {conf:.2f}"
                    
                    # Draw bounding box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    
                    # Draw label background
                    label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                    cv2.rectangle(
                        frame,
                        (x1, y1 - label_size[1] - 10),
                        (x1 + label_size[0], y1),
                        color,
                        -1,
                    )
                    
                    # Draw label text
                    cv2.putText(
                        frame,
                        label,
                        (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        2,
                    )
            
            # Calculate FPS
            loop_time = time.perf_counter() - loop_start
            fps = 1 / loop_time if loop_time > 0 else 0
            fps_list.append(fps)
            
            # Keep only last 30 frames for averaging
            if len(fps_list) > 30:
                fps_list.pop(0)
            
            avg_fps = sum(fps_list) / len(fps_list)
            
            # Draw FPS
            if show_fps:
                fps_text = f"FPS: {avg_fps:.1f}"
                cv2.putText(
                    frame,
                    fps_text,
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )
            
            # Show preview window
            if show_preview:
                # Resize for display if too large
                display_frame = frame
                if frame.shape[1] > 1280:
                    scale = 1280 / frame.shape[1]
                    display_frame = cv2.resize(frame, None, fx=scale, fy=scale)
                
                cv2.imshow("CS2 Detection", display_frame)
                
                # Check for quit
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    
    cv2.destroyAllWindows()
    print("\nDetection stopped.")
    print(f"Average FPS: {avg_fps:.1f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real-time CS2 detection")
    parser.add_argument(
        "--model",
        type=str,
        default="runs/detect/cs2_yolov8n/weights/best.pt",
        help="Path to model weights",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.1,
        help="Confidence threshold",
    )
    parser.add_argument(
        "--no-fps",
        action="store_true",
        help="Hide FPS counter",
    )
    parser.add_argument(
        "--no-preview",
        action="store_true",
        help="Disable preview window",
    )
    parser.add_argument(
        "--window",
        type=str,
        default=None,
        help="Window title to capture (partial match). Example: --window 'Counter-Strike'",
    )
    
    args = parser.parse_args()
    
    run_detection(
        model_path=args.model,
        conf_threshold=args.conf,
        show_fps=not args.no_fps,
        show_preview=not args.no_preview,
        window_title=args.window,
    )
