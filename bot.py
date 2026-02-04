"""
Simple launcher for CS2 Bot
Run with: python bot.py
"""

if __name__ == "__main__":
    from src.main import run_bot
    import argparse
    from src.config import MODEL_PATH, CONF_THRESHOLD, WINDOW_TITLE
    
    parser = argparse.ArgumentParser(description="CS2 Bot with detection and auto-aim")
    parser.add_argument("--model", type=str, default=MODEL_PATH, help="Path to model weights")
    parser.add_argument("--conf", type=float, default=CONF_THRESHOLD, help="Confidence threshold")
    parser.add_argument("--window", type=str, default=WINDOW_TITLE, help="Window title to capture")
    parser.add_argument("--no-preview", action="store_true", help="Disable preview window")
    
    args = parser.parse_args()
    
    run_bot(
        model_path=args.model,
        conf_threshold=args.conf,
        window_title=args.window,
        show_preview=not args.no_preview,
    )
