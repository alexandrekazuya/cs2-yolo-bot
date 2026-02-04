# CS2 YOLO Object Detection

Real-time enemy detection for Counter-Strike 2 using YOLOv8.

## Project Structure
```bash
cs2yolo/
├── images/             # Dataset (gitignored)
├── runs/               # Training outputs (gitignored)
├── config.py           # Configuration settings
├── controllers.py      # Input controllers (movement, aim, hotkeys)
├── detection.py        # Detection helpers
├── main.py             # Main bot entry point
├── window_capture.py   # Window capture utilities
├── train.py            # Training script
├── detect.py           # (Deprecated) Old detection script
├── capture.py          # Data collection script
└── README.md
```