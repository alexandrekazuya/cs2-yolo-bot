"""
CS2 YOLO Training Script
Optimized for RTX 3060 Ti (8GB VRAM)
"""

from ultralytics import YOLO
import argparse
from pathlib import Path


def train(
    data_yaml: str = "images/data.yaml",
    model: str = "yolov8n.pt",
    epochs: int = 100,
    imgsz: int = 640,
    batch: int = 16,
    device: int = 0,
    name: str = "cs2_yolov8n",
):
    """
    Train YOLOv8 on CS2 dataset.
    
    Args:
        data_yaml: Path to dataset configuration file
        model: Base model to use (yolov8n.pt, yolov8s.pt, etc.)
        epochs: Number of training epochs
        imgsz: Image size for training
        batch: Batch size (16 is optimal for 3060 Ti with YOLOv8n)
        device: GPU device index (0 for first GPU)
        name: Name for this training run
    """
    # Load the model
    print(f"Loading model: {model}")
    yolo = YOLO(model)
    
    # Train the model
    print(f"Starting training for {epochs} epochs...")
    print(f"Dataset: {data_yaml}")
    print(f"Image size: {imgsz}")
    print(f"Batch size: {batch}")
    
    results = yolo.train(
        data=data_yaml,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        device=device,
        name=name,
        # Optimizations for real-time detection
        augment=True,
        mosaic=1.0,
        mixup=0.1,
        # Save best model
        save=True,
        save_period=10,  # Save checkpoint every 10 epochs
        # Early stopping
        patience=20,  # Stop if no improvement for 20 epochs
        # Logging
        verbose=True,
        plots=True,
    )
    
    print("\n" + "="*50)
    print("Training complete!")
    print(f"Best model saved to: runs/detect/{name}/weights/best.pt")
    print("="*50)
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train YOLOv8 on CS2 dataset")
    parser.add_argument("--data", type=str, default="images/data.yaml", help="Path to data.yaml")
    parser.add_argument("--model", type=str, default="yolov8n.pt", help="Base model (yolov8n.pt, yolov8s.pt)")
    parser.add_argument("--epochs", type=int, default=100, help="Number of epochs")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument("--device", type=int, default=0, help="GPU device")
    parser.add_argument("--name", type=str, default="cs2_yolov8n", help="Run name")
    
    args = parser.parse_args()
    
    train(
        data_yaml=args.data,
        model=args.model,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        name=args.name,
    )
