# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import json
import logging
from pathlib import Path
import re
from typing import List

import yaml

from octoconf.components.serializers.baseline import (
    BaselineJsonEncoder,
    RuleJsonEncoder,
)
from octoconf.entities.baseline import Baseline
from octoconf.entities.rule import Rule
from octoconf.interfaces.baseline import IBaseline
from octoconf.utils.logger import *

logger = logging.getLogger(__name__)


class BaselineInterfaceAdapter(IBaseline):
    """
    Implementation of the interface allowing to work with the type of baseline.
    """

    _instance = None
    _baseline = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IBaseline, cls).__new__(cls)
        return cls._instance

    def load_baseline_from_file(self, baseline_file_path: Path) -> Baseline:
        logger.debug(f"Load baseline from {baseline_file_path}")
        base_folder = baseline_file_path.parents[0]
        rules_directory = Path(base_folder, "rules")

        if not baseline_file_path.exists():
            logger.error(
                f"The baseline file '{baseline_file_path}' has not been found or does not exists."
            )
            return None

        with open(str(baseline_file_path), "r") as checklist:
            baseline = yaml.load(checklist, Loader=yaml.SafeLoader)

        cat_cpt = 0
        for category in baseline["categories"]:
            rules_cpt = 0
            for rule in category["rules"]:
                rule_file_match = rule + "{}".format(".yaml")
                rule_file_path = Path(rules_directory, rule_file_match)
                if not rule_file_path.exists():
                    logger.error(
                        f"The rule file '{rule_file_path}' has not been found or does not exists. Removing this rule from the builded baseline."
                    )
                    del baseline["categories"][cat_cpt]["rules"][rules_cpt]
                    break

                with open(str(rule_file_path), "r") as r:
                    rule_content = yaml.load(r, Loader=yaml.SafeLoader)

                baseline["categories"][cat_cpt]["rules"][rules_cpt] = rule_content
                rules_cpt += 1
            cat_cpt += 1
        return Baseline(**baseline)

    def map_results_in_baseline(
        self, rules: List[Rule], baseline: Baseline
    ) -> Baseline:
        json_baseline = json.loads(
            json.dumps(baseline, cls=BaselineJsonEncoder, ensure_ascii=False)
        )

        for rule in rules:
            cat_cpt = 0
            for category in json_baseline["categories"]:
                rules_cpt = 0
                for og_rule in category["rules"]:
                    if og_rule["id"] == rule.id:
                        json_baseline["categories"][cat_cpt]["rules"][
                            rules_cpt
                        ] = json.loads(
                            json.dumps(rule, cls=RuleJsonEncoder, ensure_ascii=False)
                        )
                    rules_cpt += 1
                cat_cpt += 1

        return Baseline(**json_baseline)

    def get_commands(self, baseline: Baseline) -> List:
        commands = list()
        for category in baseline.categories:
            commands.append(
                {
                    "category": category.category,
                    "commands": [
                        {
                            "rule": rule.id,
                            "collection_cmd": rule.collection_cmd,
                            "check": rule.check,
                        }
                        for rule in category.rules
                    ],
                }
            )
        return commands

    def get_check(self, baseline: Baseline, rule_filename: str) -> Rule:
        for category in baseline.categories:
            for rule in category.rules:
                if rule.id == rule_filename:
                    return rule
        return None

    def update_rule_with_output_result(self, rule: Rule, output_result: str) -> Rule:
        return Rule(
            id=rule.id,
            title=rule.title,
            description=rule.description,
            collection_cmd=rule.collection_cmd,
            check=rule.check,
            verification_type=rule.verification_type,
            expected=rule.expected,
            recommendation=rule.recommendation,
            level=rule.level,
            severity=rule.severity,
            references=rule.references,
            output=output_result,
            compliant=rule.compliant,
        )

    def remove_ignore_translate_tags(self, baseline: Baseline) -> Baseline:
        json_baseline = json.loads(
            json.dumps(baseline, cls=BaselineJsonEncoder, ensure_ascii=False)
        )

        pattern, repl = r"\<\/?x\>", ""
        json_baseline["title"] = re.sub(
            pattern,
            repl,
            json_baseline["title"] if json_baseline["title"] else "",
            0,
            re.MULTILINE | re.IGNORECASE | re.DOTALL,
        )

        category_keys = ["category", "name", "description"]
        rule_keys = ["title", "description", "recommendation"]
        for category in json_baseline["categories"]:
            for category_key in category_keys:
                category[category_key] = re.sub(
                    pattern,
                    repl,
                    category[category_key] if category[category_key] else "",
                    0,
                    re.MULTILINE | re.IGNORECASE | re.DOTALL,
                )
            for rule in category["rules"]:
                for rule_key in rule_keys:
                    rule[rule_key] = re.sub(
                        pattern,
                        repl,
                        rule[rule_key] if rule[rule_key] else "",
                        0,
                        re.MULTILINE | re.IGNORECASE | re.DOTALL,
                    )

        return Baseline(**json_baseline)

    def save_translated_baseline(
        self, baseline_file_path: Path, baseline: Baseline, output_directory: Path
    ) -> int:
        baselines_submodule_path = Path.cwd() / "baselines" / "template"
        if not baselines_submodule_path.is_dir():
            logger.error(
                f"'{baselines_submodule_path}' directory does not exists. Missing 'octobaselines' module"
            )
            return 1

        rules_directory = output_directory / "rules"
        rules_directory.mkdir(parents=True, exist_ok=True)

        with open(
            baselines_submodule_path / "baseline_template.yaml", "r"
        ) as baseline_file:
            baseline_content = baseline_file.read()

        with open(
            baselines_submodule_path / "rules" / "rule_template.yaml", "r"
        ) as rule_file:
            rule_content = rule_file.read()

        # tab size = 2 (1 tab = 2 space, 3 tab = 6 space, etc.)
        # Preserve indentation otherwise yaml is not valid.
        # Category's main list sequence indentation = 2
        category_block_template = (
            2 * " " + baseline_content[baseline_content.find("- category:") :].rstrip()
        )

        # Preserve indentation otherwise yaml is not valid.
        # Category's content indentation = 6
        category_rule_block_template = (
            6 * " "
            + baseline_content[
                baseline_content.find("- MATCH_AND_REPLACE_RULE") :
            ].rstrip()
        )

        baseline_content = baseline_content[
            : baseline_content.find("- category:") :
        ].rstrip()
        category_block_template = category_block_template[
            : category_block_template.find("- MATCH_AND_REPLACE_RULE")
        ].rstrip()

        reference_block_template = (
            2 * " "
            + rule_content[
                rule_content.find("- MATCH_AND_REPLACE_REFERENCES") :
            ].rstrip()
        )

        rule_content = rule_content[
            : rule_content.find("- MATCH_AND_REPLACE_REFERENCES") :
        ].rstrip()

        baseline_content = baseline_content.replace(
            "MATCH_AND_REPLACE_TITLE", baseline.title
        )
        for category in baseline.categories:
            category_block = category_block_template
            category_block = category_block.replace(
                "MATCH_AND_REPLACE_CATEGORY", category.category
            )
            category_block = category_block.replace(
                "MATCH_AND_REPLACE_NAME", category.name
            )

            if category.description is None:
                category.description = "No description."

            # Preserve indentation otherwise yaml is not valid.
            # Category's content indentation = 6
            category_block = category_block.replace(
                "MATCH_AND_REPLACE_DESCRIPTION",
                category.description.rstrip().replace("\n", "\n" + 6 * " "),
            )

            for rule in category.rules:
                category_rule_block = category_rule_block_template
                category_rule_block = category_rule_block.replace(
                    "MATCH_AND_REPLACE_RULE", rule.id
                )
                category_block += "\n" + category_rule_block

                rule_block = rule_content
                rule_block = rule_block.replace("MATCH_AND_REPLACE_ID", rule.id)
                rule_block = rule_block.replace("MATCH_AND_REPLACE_TITLE", rule.title)
                # Preserve indentation otherwise yaml is not valid.
                # Rule's content indentation = 2
                rule_block = rule_block.replace(
                    "MATCH_AND_REPLACE_DESCRIPTION",
                    rule.description.rstrip().replace("\n", "\n" + 2 * " "),
                )
                # Preserve indentation otherwise yaml is not valid.
                # Rule's content indentation = 2
                rule_block = rule_block.replace(
                    "MATCH_AND_REPLACE_COLLECTION_CMD",
                    rule.collection_cmd.rstrip().replace("\n", "\n" + 2 * " "),
                )
                # Preserve indentation otherwise yaml is not valid.
                # Rule's content indentation = 2
                rule_block = rule_block.replace(
                    "MATCH_AND_REPLACE_CHECK",
                    rule.check.rstrip().replace("\n", "\n" + 2 * " "),
                )
                rule_block = rule_block.replace(
                    "MATCH_AND_REPLACE_VERIFICATION_TYPE", rule.verification_type
                )
                rule_block = rule_block.replace(
                    "MATCH_AND_REPLACE_EXPECTED", rule.expected
                )
                # Preserve indentation otherwise yaml is not valid.
                # Rule's content indentation = 2
                rule_block = rule_block.replace(
                    "MATCH_AND_REPLACE_RECOMMENDATION",
                    rule.recommendation.rstrip().replace("\n", "\n" + 2 * " "),
                )
                rule_block = rule_block.replace("MATCH_AND_REPLACE_LEVEL", rule.level)

                for reference in rule.references:
                    reference_block = reference_block_template
                    reference_block = reference_block.replace(
                        "MATCH_AND_REPLACE_REFERENCES", reference
                    )
                    rule_block += "\n" + reference_block

                with open(str(rules_directory / rule.id) + ".yaml", "w") as rule_file:
                    rule_file.write(rule_block)

            baseline_content += "\n" + category_block

        try:
            with open(
                str(output_directory / baseline_file_path.stem) + ".yaml", "w"
            ) as translated_baseline:
                translated_baseline.write(baseline_content)

            print(
                f"[+] Baseline successfully translated and saved in '{output_directory}'"
            )
            return 0
        except:
            logger.exception("Catch an exception while saving translated baseline.")
            return 1
