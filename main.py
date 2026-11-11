"""
Secure Image Steganography — Application Entry Point

Usage:
    python main.py
"""

import sys
import logging
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Ensure project root is on sys.path so all subpackages resolve correctly.
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_FILE = PROJECT_ROOT / "steganography.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  —  %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Security: confirm we never log passwords/keys (handled in crypto module)
logger.info("=== Secure Image Steganography starting ===")
logger.info("Log file: %s", LOG_FILE)

# ---------------------------------------------------------------------------
# Create required directories
# ---------------------------------------------------------------------------
for d in ["results", "assets/sample_images"]:
    (PROJECT_ROOT / d).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Launch GUI
# ---------------------------------------------------------------------------
try:
    from gui.main_window import MainWindow
    app = MainWindow()
    app.mainloop()
except ImportError as exc:
    print(f"\n[ERROR] Missing dependency: {exc}")
    print("Please run:  pip install -r requirements.txt\n")
    sys.exit(1)
except Exception as exc:
    logger.exception("Fatal error during startup")
    print(f"\n[FATAL] {exc}\n")
    sys.exit(1)
