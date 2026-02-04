# CS2 YOLO Object Detection

Real-time enemy detection for Counter-Strike 2 using YOLOv8.

## Project Structure
```bash
cs2yolo/
├── images/ # Dataset
│   ├── train/
│   ├── valid/
│   ├── test/
│   └── data.yaml
├── runs/ # Training outputs
│   └── detect/
│       └── cs2_yolov8n/
│           └── weights/
│               └── best.pt  # Best model
├── requirements.txt
├── train.py
├── detect.py
├── capture.py
└── README.md
```

images & runs in gitignore