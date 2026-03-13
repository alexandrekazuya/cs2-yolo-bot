# CS2 YOLO Enemy Detection

Real-time enemy detection for **Counter-Strike 2** using the YOLO object
detection architecture.

This project trains a custom object detection model to identify enemy
players in-game and integrates the model into a real-time detection
pipeline.

The system captures game frames, runs inference on a trained model, and
outputs detected enemies with bounding boxes.

------------------------------------------------------------------------

# Features

-   Custom-trained object detection model for CS2 enemies
-   Real-time inference pipeline
-   Automated dataset collection from gameplay
-   Training pipeline for object detection model
-   Modular project structure separating ML and application logic

------------------------------------------------------------------------

# How It Works

Pipeline:

game frame\
↓\
window capture\
↓\
image preprocessing\
↓\
YOLO model inference\
↓\
enemy detection\
↓\
bot/controller logic

The model was trained on a custom dataset of gameplay images labeled
with enemy bounding boxes.

------------------------------------------------------------------------

# Model Training

Training process:

1.  Collect gameplay images
2.  Label enemy positions with bounding boxes
3.  Train the YOLO model
4.  Evaluate detection performance
5.  Export trained weights for real-time inference

Example training command:

    python scripts/train.py

Training produces:

    runs/
    └── detect/
        └── train/
            ├── weights/
            │   └── best.pt
            └── results.png

The resulting weights file (`best.pt`) is used for inference.

------------------------------------------------------------------------

# Dataset

The dataset consists of gameplay screenshots containing enemy players.

Structure:

    images/
    ├── train/
    ├── val/
    └── labels/

Each image has an associated label file containing:

    class_id x_center y_center width height

Bounding boxes were manually labeled to train the detection model.

*(Dataset files are gitignored due to size.)*

------------------------------------------------------------------------

# Usage

Run the bot:

    python bot.py

Or using module syntax:

    python -m src.main

Train the model:

    python scripts/train.py

Deprecated detection script:

    python scripts/detect.py

------------------------------------------------------------------------

# Project Structure

    cs2yolo/
    ├── src/                # Bot application
    │   ├── main.py         # Main bot logic
    │   ├── config.py       # Configuration
    │   ├── controllers.py  # Input controllers
    │   ├── detection.py    # Detection helpers
    │   └── window_capture.py  # Window capture
    │
    ├── scripts/            # Utility scripts
    │   ├── train.py        # Model training
    │   ├── detect.py       # (Deprecated) Detection
    │   └── capture.py      # Data collection
    │
    ├── images/             # Dataset (gitignored)
    ├── runs/               # Training outputs (gitignored)
    │
    ├── bot.py              # Simple launcher
    └── README.md

------------------------------------------------------------------------

# Technologies

-   Python
-   PyTorch
-   OpenCV
-   YOLO

------------------------------------------------------------------------

# Future Improvements

Possible future improvements include:

-   expanding the training dataset
-   improving detection accuracy
-   adding additional object classes
-   optimizing inference latency

------------------------------------------------------------------------

# Disclaimer

This project was created for research and educational purposes related
to computer vision and machine learning.