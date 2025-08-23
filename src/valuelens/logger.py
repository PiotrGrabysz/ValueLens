import logging


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger instance."""
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        level=logging.INFO,
    )
    return logging.getLogger(name)
