# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import logging
from pathlib import Path
from typing import Any, Optional

import inject

from octoconf.decorators.decorator import Decorator
from octoconf.interfaces.baseline import IBaseline

from octoconf.utils.logger import *

logger = logging.getLogger(__name__)


class BaselineDecorator(Decorator):
    """
    Allows the user to submit the title of an existing baseline and not the full path. This decorator returns the path of the baseline if any.
    """

    adapter = inject.attr(IBaseline)

    def __init__(self) -> None:
        pass

    def decorator(func) -> Any:
        def inner(*args, **kwargs):
            def get_path_of_baseline(l, f) -> Optional[Path]:
                for d in l:
                    if f(d["title"]) or f(d["filename"]):
                        return d["path"]
                return None

            def get_path_of_util_script(l, f) -> Optional[Path]:
                for d in l:
                    if f(d["filename"]):
                        return d["path"]
                return None

            baseline_path = get_path_of_baseline(
                BaselineDecorator().adapter.list_available_baselines(),
                lambda v: v == args[0].baseline,
            )
            if baseline_path:
                args[0].baseline = baseline_path

            utility_script_path = get_path_of_util_script(
                BaselineDecorator().adapter.list_available_utils_scripts(),
                lambda v: v == args[0].utils,
            )
            if utility_script_path:
                args[0].utils = utility_script_path

            return func(*args, **kwargs)

        return inner
