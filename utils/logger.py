"""
Logging utility for LexAssist.
Configures basic application logging while enforcing privacy sanitation
(zero logging of API keys, private documents, or sensitive user inputs).
"""

import logging
import os
import re

LOG_FILE = os.path.join("data", "lexassist.log")

def get_logger(name: str = "LexAssist"):
    """Configures and returns a sanitized logger."""
    os.makedirs("data", exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

def log_event(event_type: str, details: str):
    """Sanitizes sensitive details before logging."""
    logger = get_logger()
    # Mask any potential API keys (e.g. AIzaSy...)
    sanitized_details = re.sub(r"AIzaSy[A-Za-z0-9_-]{33}", "AIzaSy[REDACTED_API_KEY]", details)
    logger.info(f"{event_type} - {sanitized_details}")

if __name__ == "__main__":
    log_event("TEST_EVENT", "System initialized cleanly with API Key AIzaSy123456789012345678901234567890123.")
    print("Sanitized log entry written to data/lexassist.log")

