# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import json
import logging
from pathlib import Path
import re
import shutil
from typing import List
import zipfile

import yaml

from octoconf.components.serializers.baseline import (
    BaselineJsonEncoder,
    RuleJsonEncoder,
)
from octoconf.entities.baseline import Baseline
from octoconf.entities.rule import Rule
from octoconf.interfaces.baseline import IBaseline
from octoconf.utils.logger import *

from octoconf.utils.timestamp import timestamp

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
            try:
                baseline = yaml.load(checklist, Loader=yaml.SafeLoader)
            except:
                logger.exception(f"Unable to load the file '{baseline_file_path}'")

        try:
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
        except:
            # No log here on purpose
            return None

        return Baseline(**baseline)

    def list_available_baselines(self) -> list:
        base_dir = Path(__file__).resolve().parent.parent.parent
        baselines_dir = base_dir / "baselines"

        available_baselines = []
        allowed_extensions = { ".yaml", ".yml" }

        for _, file in enumerate(baselines_dir.glob(r"**/*")):
            if not file.suffix in allowed_extensions:
                continue

            # We only need the "root" file, not the rules nor the template
            if not "rules" in str(file) and not "template" in str(file):
                try:
                    logger.debug(f"Found baseline candidate: '{file}'")
                    baseline = self.load_baseline_from_file(file)
                    if baseline is None:
                        continue

                    if "custom" in str(file):
                        available_baselines.append(
                            {
                                "title": baseline.title,
                                "path": file,
                                "filename": file.name,
                                "source": "Imported",
                            }
                        )
                    else:
                        available_baselines.append(
                            {
                                "title": baseline.title,
                                "path": file,
                                "filename": file.name,
                                "source": "Built-in",
                            }
                        )
                except:
                    logger.exception(
                        f"Something went wrong when listing available baselines for file '{file}'"
                    )
                    continue

        return available_baselines

    def export_custom_baselines(self) -> str:
        try:
            archive_name = Path.cwd() / f"octoconf_baselines_export_{timestamp()}"
            root_dir = Path(__file__).resolve().parent.parent.parent / "baselines"
            base_dir = "custom"

            return shutil.make_archive(
                archive_name, "zip", root_dir=str(root_dir), base_dir=base_dir
            )
        except:
            logger.exception("Unable to export custom baselines")
            return None

    def import_custom_baselines_from_archive(self, archive: str, action: str) -> Path:
        logger.info(
            f"Importing custom baselines from '{archive}' with action '{action}'"
        )
        extract_dir = Path(__file__).resolve().parent.parent.parent / "baselines"
        custom_baselines_dir = extract_dir / "custom"
        custom_baselines_tmp_dir = extract_dir / "custom_tmp"

        try:
            if custom_baselines_tmp_dir.exists():
                shutil.rmtree(custom_baselines_tmp_dir)
            logger.info("Saving the original state")
            shutil.copytree(custom_baselines_dir, custom_baselines_tmp_dir)
        except Exception as e:
            logger.exception(f"Catch exception {e}")
            return None

        # switch case 'match value: case value:' needs python 3.10
        # the tool must work with python 3.8
        if action.lower() == "merge":
            try:
                with zipfile.ZipFile(archive, "r") as zip_ref:
                    for zip_info in zip_ref.infolist():
                        file_path = Path(extract_dir) / zip_info.filename
                        if zip_info.is_dir():
                            file_path.mkdir(parents=True, exist_ok=True)
                        else:
                            with zip_ref.open(zip_info) as source, file_path.open(
                                "wb"
                            ) as target:
                                target.write(source.read())
            except:
                logger.exception("Unable to extract and merge custom baselines")
                logger.info("Rollback the original state")
                if custom_baselines_dir.exists():
                    shutil.rmtree(custom_baselines_dir)

                shutil.move(custom_baselines_tmp_dir, custom_baselines_dir)
                return None
        else:
            try:
                if custom_baselines_dir.exists():
                    shutil.rmtree(custom_baselines_dir)

                with zipfile.ZipFile(archive, "r") as zip_ref:
                    if not "custom" in zip_ref.infolist()[0].filename.lower():
                        custom_baselines_dir.mkdir(parents=True)
                        zip_ref.extractall(custom_baselines_dir)
                    else:
                        zip_ref.extractall(extract_dir)
            except:
                logger.exception("Unable to extract and replace custom baselines")
                logger.info("Rollback the original state")
                if custom_baselines_dir.exists():
                    shutil.rmtree(custom_baselines_dir)

                shutil.move(custom_baselines_tmp_dir, custom_baselines_dir)
                return None

        # Everything went well, the temporary directory can be removed
        try:
            logger.info("Removing the temporary directory")
            shutil.rmtree(custom_baselines_tmp_dir)
        except:
            logger.exception("Unable to remove temporary directory")
        finally:
            return extract_dir / "custom"

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
        tab_size = 2
        # Preserve indentation otherwise yaml is not valid.
        # Category's main list sequence indentation = 2
        category_block_template = (
            tab_size * " " + baseline_content[baseline_content.find("- category:") :].rstrip()
        )

        # Preserve indentation otherwise yaml is not valid.
        # Category's content indentation = 6
        category_rule_block_template = (
            (tab_size * 3) * " "
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
            tab_size * " "
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
                category.description.rstrip().replace("\n", "\n" + (tab_size * 3) * " "),
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
                    rule.description.rstrip().replace("\n", "\n" + tab_size * " "),
                )
                # Preserve indentation otherwise yaml is not valid.
                # Rule's content indentation = 2
                rule_block = rule_block.replace(
                    "MATCH_AND_REPLACE_COLLECTION_CMD",
                    rule.collection_cmd.rstrip().replace("\n", "\n" + tab_size * " "),
                )
                # Preserve indentation otherwise yaml is not valid.
                # Rule's content indentation = 2
                rule_block = rule_block.replace(
                    "MATCH_AND_REPLACE_CHECK",
                    rule.check.rstrip().replace("\n", "\n" + tab_size * " "),
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
                    rule.recommendation.rstrip().replace("\n", "\n" + tab_size * " "),
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
