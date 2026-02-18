"""
Configuration file for CS2 Bot
All configurable constants in one place
"""

from pynput import keyboard

# Global hotkey to toggle bot (F6 by default)
TOGGLE_HOTKEY = keyboard.Key.f6

# Model configuration
MODEL_PATH = "runs/detect/runs/detect/cs2_yolov8s/weights/best.pt"
CONF_THRESHOLD = 0.1
WINDOW_TITLE = "Counter-Strike"

# Movement settings
MOVE_INTERVAL = 1  # Seconds between direction changes
MOVE_KEYS = ['a', 'd']

# Aim settings
AIM_SPEED = 2.5  # Mouse sensitivity multiplier

SHOOT_COOLDOWN = 0.22
BODY_OFFSET = 0.2  # Distance from top of box to aim (0.0=top, 0.5=center, 0.2=neck)
HEAD_OFFSET = 0.5 # Distance from top of head box (0.0=top, 0.5=center, 0.15=forehead)

# Class IDs
HEAD_CLASSES = [1, 3]  # CT_HEAD, T_HEAD
BODY_CLASSES = [0, 2]  # CT, T
