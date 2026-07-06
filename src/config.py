from pathlib import Path

# Root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

#Data
RAW_DATA_DIR = PROJECT_ROOT / " data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

# Models
MODEL_DIR = PROJECT_ROOT / "models"

# Reports
REPORT_DIR = PROJECT_ROOT / "reports"

# Test split and shuffling
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Dataset Name and target column
DATASET_NAME = "Motor vehicle insurance data.csv"
