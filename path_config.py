"""Centralized path configuration for the IdentifyTheAuthor project.
Import this module in notebooks / scripts to avoid hardcoded paths.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
TRAIN_CSV = DATA_DIR / "train" / "train.csv"
TEST_CSV = DATA_DIR / "test" / "test.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
MODELS_DIR = OUTPUT_DIR / "models"

# Ensure directories exist
for d in (OUTPUT_DIR, MODELS_DIR):
    d.mkdir(parents=True, exist_ok=True)

