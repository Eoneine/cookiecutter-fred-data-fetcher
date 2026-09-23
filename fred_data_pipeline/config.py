import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")
if not FRED_API_KEY:
    raise EnvironmentError(
        "FRED_API_KEY is not set. "
        "Please add it to your .env file or set it as an environment variable."
    )
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

PROJ_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

SERIES_IDS = ["GDP", "UNRATE", "CPIAUCSL"]  # can be changed/extended

# The user-facing choice: "long" or "wide"
OUTPUT_FORMAT = "long"
