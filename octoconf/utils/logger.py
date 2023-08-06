# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import logging
import logging.handlers
from os import getenv
from pathlib import Path
import platform
import time


def get_log_file() -> Path:
    if platform.system() == "Windows":
        basedir = Path(getenv("LOCALAPPDATA") / "octoconf")
    else:
        basedir = Path.home() / ".cache" / "octoconf"
    basedir.mkdir(parents=True, exist_ok=True)
    return basedir / "octoconf.log"


def init_logging(loglevel: str) -> None:
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("[x] Error! Invalid log level: %s" % loglevel)

    log_handler = logging.handlers.RotatingFileHandler(
        get_log_file(), mode="a", maxBytes=50000000, backupCount=5, encoding="utf-8"
    )
    formatter = logging.Formatter(
        "%(asctime)s : %(levelname)s : %(name)s : %(message)s", "%b %d %H:%M:%S"
    )
    # UTC time
    formatter.converter = time.gmtime
    log_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(numeric_level)
