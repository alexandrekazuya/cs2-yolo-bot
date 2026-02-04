CS2 Bot Code Refactoring - Walkthrough
Overview
The bot code has been refactored from a single monolithic file (
bot.py
) into a clean modular structure for better maintainability and organization.

New File Structure
config.py
Purpose: Centralized configuration

All tunable constants (model path, hotkeys, movement settings, aim settings)
Easy to modify without touching core logic
HEADSHOT_OFFSET = 0.37 controls vertical aim adjustment
window_capture.py
Purpose: Window management and screen capture

find_window()
 - Locate CS2 window
capture_window()
 - Capture window frames
is_game_focused()
 - Check if game has focus
controllers.py
Purpose: Input control classes

HotkeyListener
 - Global F6 toggle
MovementController
 - A/D strafing logic
AimController
 - Mouse movement and shooting
detection.py
Purpose: YOLO detection utilities

get_closest_enemy()
 - Find nearest target to crosshair
main.py
Purpose: Main entry point

Orchestrates all modules
Main bot loop
Command-line argument parsing
Running the Bot
The refactored bot works exactly the same as before:

# Basic usage
python main.py
# With custom settings
python main.py --conf 0.25 --window "Counter-Strike"
