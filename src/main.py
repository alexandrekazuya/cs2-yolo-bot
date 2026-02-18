"""
CS2 Bot - Main Entry Point
Moves with A/D, detects enemies, aims and shoots automatically.
WARNING: Use at your own risk. This may violate game TOS.
"""

import cv2
import time
from ultralytics import YOLO

from src.config import (
    MODEL_PATH, CONF_THRESHOLD, WINDOW_TITLE, 
    SHOOT_COOLDOWN, BODY_OFFSET, HEAD_OFFSET, 
    BODY_CLASSES, HEAD_CLASSES,
)
from src.window_capture import find_window, capture_window, is_game_focused, cleanup_camera
from src.controllers import HotkeyListener, MovementController, AimController
from src.detection import get_closest_enemy


def run_bot(
    model_path: str = MODEL_PATH,
    conf_threshold: float = CONF_THRESHOLD,
    window_title: str = WINDOW_TITLE,
    show_preview: bool = True,
):
    """Run the bot with detection and input control."""

    print(f"\nLoading model: {model_path}")
    
    model = YOLO(model_path)
    model.to('cuda')
    class_names = model.names
    print(f"Classes: {class_names}")
    
    # Find game window
    windows = find_window(window_title)
    if not windows:
        print(f"ERROR: Window '{window_title}' not found!")
        return
    
    target_hwnd, found_title = windows[0]
    print(f"Found window: {found_title}")
    
    # Get initial frame to determine dimensions
    frame, width, height = capture_window(target_hwnd)
    if frame is None:
        print("ERROR: Could not capture window!")
        return
    
    print(f"Window size: {width}x{height}")
    print("\nControls:")
    print("  Press 'q' in preview to quit")
    print("  Press 'F6' anywhere to pause/resume bot")
    print("-" * 50)
    
    # Initialize controllers
    movement = MovementController()
    aim = AimController(width, height)
    
    # Bot state
    bot_state = {'active': True}
    
    def toggle_bot():
        """Toggle bot active state."""
        bot_state['active'] = not bot_state['active']
        status = "resumed" if bot_state['active'] else "paused"
        print(f"Bot {status}")
        if not bot_state['active']:
            movement.stop()
        else:
            movement.start()
    
    # Start hotkey listener
    hotkey = HotkeyListener(toggle_bot)
    hotkey.start()
    
    # Start movement
    movement.start()
    print("Bot started! Strafing with A/D...")
    
    fps_list = []
    last_shot_time = 0
    preview_frame_counter = 0
    # Aim prediction state
    prev_target_x = None
    prev_target_time = None
    velocity_x = 0.0
    EMA_ALPHA = 0.7
    LEAD_FACTOR = 4.1
    MIN_VELOCITY = 50
    direction_history = []  # Track velocity direction to detect oscillation
    locked_direction = 0  # Locked prediction direction (+1/-1/0)
    CONSISTENCY_FRAMES = 5  # Require N consistent direction frames before predicting
    PREDICTION_RADIUS = 70

    try:
        while True:
            loop_start = time.perf_counter()
            
            # Capture frame
            t0 = time.perf_counter()
            frame, _, _ = capture_window(target_hwnd)
            t1 = time.perf_counter()
            if frame is None:
                print("Window closed or minimized.")
                break
            
            # Run detection
            results = model(frame, conf=conf_threshold, verbose=False, half=True)
            t2 = time.perf_counter()
            capture_ms = (t1 - t0) * 1000
            infer_ms = (t2 - t1) * 1000
            
            # Process detections
            detections = []
            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    cls_id = int(box.cls[0])
                    detections.append((x1, y1, x2, y2, conf, cls_id))
            
            # If bot is active and enemies detected, aim and shoot
            current_time = time.perf_counter()
            
            # Check if game window is focused (bot only works when in-game)
            game_focused = is_game_focused(window_title)
            
            if bot_state['active'] and detections and game_focused:
                target = get_closest_enemy(detections, width // 2, height // 2)
                if target:
                    # Unpack target data
                    center_x, center_y, x1, y1, x2, y2, _, cls_id = target
                    
                    target_x = center_x
                    target_y = center_y
                    
                    # If aiming at body, adjust vertical aim to head level
                    if int(cls_id) in BODY_CLASSES:
                        box_height = y2 - y1
                        target_y = y1 + (box_height * BODY_OFFSET)
                    elif int(cls_id) in HEAD_CLASSES:
                        box_height = y2 - y1
                        target_y = y1 + (box_height * HEAD_OFFSET)
                    
                    # --- Aim prediction: horizontal only ---
                    if prev_target_x is not None and prev_target_time is not None:
                        dt = current_time - prev_target_time
                        if 0 < dt < 0.5:
                            raw_vx = (center_x - prev_target_x) / dt
                            velocity_x = EMA_ALPHA * raw_vx + (1 - EMA_ALPHA) * velocity_x
                            
                            # Track direction: +1 right, -1 left, 0 slow
                            cur_dir = 0
                            if abs(velocity_x) > MIN_VELOCITY:
                                cur_dir = 1 if velocity_x > 0 else -1
                            direction_history.append(cur_dir)
                            if len(direction_history) > 6:
                                direction_history.pop(0)
                            
                            # Lock direction once consistent, keep it until opposite is consistent
                            recent = direction_history[-CONSISTENCY_FRAMES:]
                            if len(recent) == CONSISTENCY_FRAMES and all(d == recent[0] and d != 0 for d in recent):
                                locked_direction = recent[0]
                            
                            dist_from_center = abs(center_x - width // 2)
                            predict_scale = max(0.0, 1.0 - dist_from_center / PREDICTION_RADIUS)
                            
                            # Predict using locked direction with current velocity magnitude
                            if locked_direction != 0:
                                lead_time = dt * LEAD_FACTOR * predict_scale
                                target_x += abs(velocity_x) * locked_direction * lead_time
                        else:
                            velocity_x = 0.0
                            direction_history.clear()
                            locked_direction = 0
                    
                    prev_target_x = center_x
                    prev_target_time = current_time
                    
                    # Pause movement while aiming
                    movement.pause()
                    
                    # Aim at target
                    aim.aim_at_target(target_x, target_y)
                    
                    # Shoot only if cooldown has passed
                    if current_time - last_shot_time >= SHOOT_COOLDOWN:
                        aim.shoot()
                        last_shot_time = current_time
                else:
                    # Resume movement if no valid target
                    movement.resume()
                    prev_target_x = None
                    prev_target_time = None
                    velocity_x = 0.0
                    direction_history.clear()
                    locked_direction = 0
                    
            else:
                # Pause if bot inactive or game not focused, otherwise resume movement
                if not bot_state['active'] or not game_focused:
                    movement.pause()
                else:
                    movement.resume()
                prev_target_x = None
                prev_target_time = None
                velocity_x = 0.0
                direction_history.clear()
                locked_direction = 0
            
            # FPS tracking (always, not just when preview is on)
            fps = 1 / (time.perf_counter() - loop_start) if (time.perf_counter() - loop_start) > 0 else 0
            fps_list.append(fps)
            if len(fps_list) > 30:
                fps_list.pop(0)
            avg_fps = sum(fps_list) / len(fps_list)

            # Draw preview (only every 3 frames to avoid waitKey overhead)
            preview_frame_counter += 1
            if show_preview and preview_frame_counter % 3 == 0:
                display = frame.copy()
                
                # Draw crosshair
                cv2.line(display, (width//2 - 20, height//2), (width//2 + 20, height//2), (0, 255, 0), 2)
                cv2.line(display, (width//2, height//2 - 20), (width//2, height//2 + 20), (0, 255, 0), 2)
                
                # Draw detections
                for det in detections:
                    x1, y1, x2, y2, conf, cls_id = det
                    color = (0, 0, 255)
                    cv2.rectangle(display, (x1, y1), (x2, y2), color, 2)
                    label = f"{class_names[cls_id]}: {conf:.2f}"
                    cv2.putText(display, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                # Draw status
                if not game_focused:
                    status = "GAME NOT FOCUSED - BOT PAUSED"
                    status_color = (0, 165, 255)
                elif bot_state['active']:
                    status = "BOT ACTIVE (F6 to pause)"
                    status_color = (0, 255, 0)
                else:
                    status = "BOT PAUSED (F6 to resume)"
                    status_color = (0, 0, 255)
                cv2.putText(display, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
                cv2.putText(display, f"FPS: {avg_fps:.1f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(display, f"Capture: {capture_ms:.0f}ms | Infer: {infer_ms:.0f}ms", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)
                
                # Resize and show
                if display.shape[1] > 1280:
                    scale = 1280 / display.shape[1]
                    display = cv2.resize(display, None, fx=scale, fy=scale)
                
                cv2.imshow("CS2 Bot", display)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
    
    finally:
        hotkey.stop()
        movement.stop()
        cleanup_camera()
        cv2.destroyAllWindows()
        print("\nBot stopped.")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="CS2 Bot with detection and auto-aim")
    parser.add_argument("--model", type=str, default=MODEL_PATH, help="Path to model weights")
    parser.add_argument("--conf", type=float, default=CONF_THRESHOLD, help="Confidence threshold")
    parser.add_argument("--window", type=str, default=WINDOW_TITLE, help="Window title to capture")
    parser.add_argument("--no-preview", action="store_true", help="Disable preview window")
    
    args = parser.parse_args()
    
    run_bot(
        model_path=args.model,
        conf_threshold=args.conf,
        window_title=args.window,
        show_preview=not args.no_preview,
    )
