# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from pathlib import Path
from typing import Any

import inject

from octoconf.interfaces.baseline import IBaseline
from octoconf.interfaces.generate_report import IReportGenerator


class GenerateReportUseCase:
    """
    This use case will allow to call the report generator facilitating the manual processing of the audit results.
    """

    @inject.autoparams("baseline_adapter", "report_generator")
    def __init__(self, baseline_adapter: IBaseline, report_generator: IReportGenerator) -> None:
        self._baseline_adapter = baseline_adapter
        self._report_generator = report_generator

    def execute(
            self,
            data_input: Any,
            args: Any,
            recompile: bool = False) -> int:
        if recompile:
            if Path(data_input).is_file():
                return self._report_generator.regenerate_report(Path(data_input), args)
            else:
                return 1
        else:
            baseline = self._baseline_adapter.load_baseline_from_file(Path(args.baseline))
            if baseline is None:
                return 1

            return self._report_generator.generate_report(
                self._baseline_adapter.remove_ignore_translate_tags(
                    self._baseline_adapter.map_results_in_baseline(
                        data_input,
                        baseline
                    )
                ), args
            )
