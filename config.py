"""
Configuration file for CS2 Bot
All configurable constants in one place
"""

from pynput import keyboard

# Global hotkey to toggle bot (F6 by default)
TOGGLE_HOTKEY = keyboard.Key.f6

# Model configuration
MODEL_PATH = "runs/detect/cs2_yolov8n/weights/best.pt"
CONF_THRESHOLD = 0.3
WINDOW_TITLE = "Counter-Strike"

# Movement settings
MOVE_INTERVAL = 1  # Seconds between direction changes
MOVE_KEYS = ['a', 'd']

# Aim settings
AIM_SPEED = 2.0  # Mouse sensitivity multiplier
SHOOT_COOLDOWN = 0.22  # Cooldown between shots (seconds)
HEADSHOT_OFFSET = 0.3  # Vertical offset multiplier for headshot aim (0.0-1.0)
