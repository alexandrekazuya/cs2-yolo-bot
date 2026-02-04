# CS2 YOLO Object Detection

Real-time enemy detection for Counter-Strike 2 using YOLOv8.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note**: For GPU acceleration, ensure you have the correct PyTorch CUDA version installed. Visit https://pytorch.org for installation instructions.

### 2. Verify Installation

```bash
python -c "from ultralytics import YOLO; import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

## Usage

### Training

Train the model on your dataset:

```bash
# Basic training (YOLOv8n - fastest)
python train.py

# With custom parameters
python train.py --model yolov8s.pt --epochs 150 --batch 12

# All options
python train.py --help
```

### Real-Time Detection

After training, run detection:

```bash
# Use the best trained model
python detect.py

# With custom model and confidence
python detect.py --model runs/detect/cs2_yolov8n/weights/best.pt --conf 0.6

# All options
python detect.py --help
```

Press `q` to quit detection.

### Capture Screenshots (Optional)

Collect more training data:

```bash
python capture.py
```

Press `c` to capture, `q` to quit.

## Project Structure

```
cs2yolo/
├── CS2.v2i.yolov8/      # Dataset from Roboflow
│   ├── train/
│   ├── valid/
│   ├── test/
│   └── data.yaml
├── runs/                 # Training outputs
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

## Configuration

### Model Options

| Model | Speed | Accuracy | Use Case |
|-------|-------|----------|----------|
| `yolov8n.pt` | ⚡⚡⚡ | Good | Real-time, default |
| `yolov8s.pt` | ⚡⚡ | Better | If accuracy is low |
| `yolov8m.pt` | ⚡ | Great | High-end GPU |

### Training Parameters

- `--epochs`: More epochs = better accuracy (default: 100)
- `--batch`: Higher = faster training, but more VRAM (default: 16)
- `--imgsz`: Image size, 640 is standard (default: 640)

## Tips

1. **Low accuracy?** Try more epochs or use `yolov8s.pt`
2. **Out of memory?** Reduce batch size: `--batch 8`
3. **Slow detection?** Reduce confidence: `--conf 0.3`
4. **Need more data?** Use `capture.py` and annotate on Roboflow
