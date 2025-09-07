import logging
import os

LEVEL = logging.INFO
if debug_mode := os.getenv("VALUELENS_DEBUG", "0") == "1":
    LEVEL = logging.DEBUG


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger instance."""
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        level=LEVEL,
    )
    return logging.getLogger(name)
