from ultralytics import YOLO

if __name__ == '__main__':
    # Load a pretrained YOLOv8s model
    model = YOLO('yolov8s.pt')

    # Train the model
    model.train(
        data='images/data.yaml',
        imgsz=960,
        epochs=200,
        batch=-1,        # Auto batch size
        cos_lr=True,     # Cosine learning rate scheduler
        save=True,       # Save checkpoints
        project='runs/detect',
        name='cs2_yolov8s',
        exist_ok=True,    # Allow overwriting existing project/name if needed, or better False to create new run dir
        # default augmentations are already active in YOLOv8
        # horizontal_flip is fliplr, default is 0.5. Removing invalid arg.
        mosaic=1.0,           # mosaic=1.0 (default)
        hsv_h=0.015,          # default
        hsv_s=0.7,            # default
        hsv_v=0.4,            # default
        scale=0.5,            # scale=0.5 (default)
    )
