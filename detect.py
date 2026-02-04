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


def run_detection(
    model_path: str = "runs/detect/cs2_yolov8n/weights/best.pt",
    conf_threshold: float = 0.5,
    show_fps: bool = True,
    show_preview: bool = True,
):
    """
    Run real-time detection on screen capture.
    
    Args:
        model_path: Path to trained model weights
        conf_threshold: Confidence threshold for detections
        show_fps: Show FPS counter on screen
        show_preview: Show detection preview window
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
    
    with mss.mss() as sct:
        region = get_capture_region(sct)
        print(f"Capture region: {region['width']}x{region['height']}")
        
        while True:
            loop_start = time.perf_counter()
            
            # Capture screen
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
        default=0.5,
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
    
    args = parser.parse_args()
    
    run_detection(
        model_path=args.model,
        conf_threshold=args.conf,
        show_fps=not args.no_fps,
        show_preview=not args.no_preview,
    )
