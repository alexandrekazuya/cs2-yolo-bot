# CS2 YOLO Object Detection

Real-time enemy detection for Counter-Strike 2 using YOLOv8.

## Usage

```bash
# Run the bot
python bot.py

# Or use module syntax
python -m src.main

# Train the model
python scripts/train.py

# Use detection script (deprecated, use bot.py instead)
python scripts/detect.py
```

## Project Structure
```bash
cs2yolo/
├── src/                # Bot application
│   ├── main.py         # Main bot logic
│   ├── config.py       # Configuration
│   ├── controllers.py  # Input controllers
│   ├── detection.py    # Detection helpers
│   └── window_capture.py  # Window capture
├── scripts/            # Utility scripts
│   ├── train.py        # Model training
│   ├── detect.py       # (Deprecated) Detection
│   └── capture.py      # Data collection
├── images/             # Dataset (gitignored)
├── runs/               # Training outputs (gitignored)
├── bot.py              # Simple launcher
└── README.md
```