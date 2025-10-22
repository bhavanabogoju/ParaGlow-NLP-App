# src/logger.py
import logging
import os
from src.utils import load_config

# Load config to get log file path
try:
    config = load_config()
    LOG_FILE_PATH = config['artifacts']['log_file_path']
except Exception as e:
    print(f"Error loading config for logger: {e}. Defaulting log path.")
    LOG_FILE_PATH = "logs/default.log"

# Ensure the logs directory exists
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

# Set up the logger
logging.basicConfig(
    level=logging.INFO,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH), # Log to a file
        logging.StreamHandler()             # Log to the console (terminal)
    ]
)

# Create a logger instance
logger = logging.getLogger("SummarizerAppLogger")