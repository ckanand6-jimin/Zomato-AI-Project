from __future__ import annotations

import logging


def configure_logging(level: int = logging.INFO) -> None:
    fmt = "%(asctime)s %(levelname)-8s [%(name)s] %(message)s"
    logging.basicConfig(level=level, format=fmt)
    # reduce verbosity for noisy libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("groq").setLevel(logging.WARNING)
