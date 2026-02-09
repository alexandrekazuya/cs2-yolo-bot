### Training

#Basic training (YOLOv8n - fastest)
```bash
python train.py
```

# With custom parameters
```bash
python train.py --model yolov8s.pt --epochs 150 --batch 12

#All options
python train.py --help
```

### Real-Time Detection

After training, run detection:
```bash
#use the best trained model
python detect.py

#With custom model and confidence
python detect.py --model runs/detect/cs2_yolov8n/weights/best.pt --conf 0.6

Press `q` to quit detection.

python detect.py --window "Counter-Strike 2"

Note: Some games with anti-cheat may block window capture via PrintWindow. If you get a black screen, full-screen capture (without --window) will still work.

### Capture Screenshots

Collect more training data:

```bash
python capture.py
```

Press `c` to capture, `q` to quit.

### Training Parameters

- `--epochs`: More epochs = better accuracy (default: 100)
- `--batch`: Higher = faster training, but more VRAM (default: 16)
- `--imgsz`: Image size, 640 is standard (default: 640)

1. **Low accuracy?** Try more epochs or use `yolov8s.pt`
2. **Out of memory?** Reduce batch size: `--batch 8`
3. **Slow detection?** Reduce confidence: `--conf 0.3`
4. **Need more data?** Use `capture.py` and annotate on Roboflow

Datasets used: 
 - https://universe.roboflow.com/cs2-imagens-p-bot/myproject-cnbvt-oeadt (11k images)
 - My own captures (1.6k images)