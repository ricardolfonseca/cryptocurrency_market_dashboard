import logging
import json
import os
from datetime import datetime

class CustomFormatter(logging.Formatter):
    """
    Custom logging formatter to include milliseconds in the timestamp.
    """
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created)
        return dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Keeps 3 decimal places for milliseconds

def configure_logging():
    """
    Configures logging to write to a file and console.
    - Logs are written to 'exchange.log' with DEBUG level.
    """
    log_format = '[%(asctime)s] [%(levelname)s] %(message)s'
    formatter = CustomFormatter(log_format)

    # File handler to write logs to 'exchange.log'
    file_handler = logging.FileHandler("exchange.log", mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler for live debugging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Configure logging
    logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, console_handler])

# Global variable to avoid repeated warnings
_config_loaded = False

def load_config():
    """
    Loads API configuration from a JSON file.
    - If 'config/config.json' exists, it loads the settings.
    - If the file is missing, it logs a warning **only once** and returns default settings.
    """
    global _config_loaded
    config_file = "config/config.json"

    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            return json.load(file)

    # Show the warning only the first time
    if not _config_loaded:
        logging.warning("Config file not found. Using defaults.")
        _config_loaded = True

    return {"base_url": "https://api.coingecko.com/api/v3/"}  # Default API URL

def current_date():
    """
    Returns the current date formatted as YYYYMMDD (e.g., '20250309' for March 9, 2025).
    """
    return datetime.now().strftime('%Y%m%d')