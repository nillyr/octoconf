# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import sys

import pytest

sys.path.append("../../octoconf/")
from octoconf.interface_adapters.generate_script.unix_bash_script import (
    UnixBashScript,
)
from octoconf.interface_adapters.generate_script.windows_powershell_script import (
    WindowsPowershellScript,
)


@pytest.fixture
def unix_content():
    return [
        {
            "category": "a category with space",
            "commands": [
                {
                    "rule": "rule_id",
                    "collection_cmd": "ls -al > ls.txt",
                    "check": "whoami",
                }
            ],
        }
    ]


@pytest.fixture
def unix_content_with_multiple_output():
    return [
        {
            "category": "a category with space",
            "commands": [
                {
                    "rule": "rule_id",
                    "collection_cmd": "[[ -f file.conf ]] && cat file.conf > dummy_1.txt; cat file2.conf >> dummy_2.txt",
                    "check": "whoami",
                }
            ],
        }
    ]


@pytest.fixture
def windows_content():
    return [
        {
            "category": "a category with space",
            "commands": [
                {
                    "rule": "rule_id",
                    "collection_cmd": "dir > dir.txt",
                    "check": "whoami /all",
                }
            ],
        }
    ]


@pytest.fixture
def windows_powershell_cmdlet_content_1():
    return [
        {
            "category": "a category with space",
            "commands": [
                {
                    "rule": "rule_id",
                    "collection_cmd": "dir | Out-File -Encoding utf8 -FilePath dir.txt",
                    "check": "whoami /all",
                }
            ],
        }
    ]


@pytest.fixture
def windows_powershell_cmdlet_content_2():
    return [
        {
            "category": "a category with space",
            "commands": [
                {
                    "rule": "rule_id",
                    "collection_cmd": "dir | Out-File -Encoding utf8 -Append -FilePath dir.txt",
                    "check": "whoami /all",
                }
            ],
        }
    ]


@pytest.fixture
def windows_powershell_cmdlet_content_3():
    return [
        {
            "category": "a category with space",
            "commands": [
                {
                    "rule": "rule_id",
                    "collection_cmd": "dir | Out-File -Append -Encoding utf8 -FilePath dir.txt",
                    "check": "whoami /all",
                }
            ],
        }
    ]


@pytest.fixture
def collect_only_and_not_only():
    return [
        {
            "category_id": 1,
            "category_name": "a category with space",
            "checks_cmds": [["1.1.1", ""]],
            "collection_cmds": ["dir > dir.txt"],
        },
        {
            "category_id": 2,
            "category_name": "a category with space",
            "checks_cmds": [["2.1.1", "whoami /all"]],
            "collection_cmds": ["net user > net_user.txt"],
        },
    ]


def test_write_script_for_linux(unix_content):
    # fmt:off
    expected_output = '\nCATEGORY="a_category_with_space"\necho "[*] Starting Collection commands of category: ${CATEGORY}..."\nmkdir -p "${BASEDIR}"/"${CATEGORY}"/\nls -al > "${BASEDIR}"/"${CATEGORY}"/ls.txt\n'
    # fmt:on

    linux_sh = UnixBashScript()
    cmds = linux_sh.write_script("", unix_content, linux_sh.write_checks_cmds)

    assert expected_output in cmds


def test_write_script_for_linux_with_multiple_output(unix_content_with_multiple_output):
    # fmt:off
    expected_output = '\nCATEGORY="a_category_with_space"\necho "[*] Starting Collection commands of category: ${CATEGORY}..."\nmkdir -p "${BASEDIR}"/"${CATEGORY}"/\n[[ -f file.conf ]] && cat file.conf > "${BASEDIR}"/"${CATEGORY}"/dummy_1.txt; cat file2.conf >> "${BASEDIR}"/"${CATEGORY}"/dummy_2.txt\n'
    # fmt:on

    linux_sh = UnixBashScript()
    cmds = linux_sh.write_script(
        "", unix_content_with_multiple_output, linux_sh.write_checks_cmds
    )

    assert expected_output in cmds


def test_write_script_for_mac(unix_content):
    # fmt:off
    expected_output = '\nCATEGORY="a_category_with_space"\necho "[*] Starting Collection commands of category: ${CATEGORY}..."\nmkdir -p "${BASEDIR}"/"${CATEGORY}"/\nls -al > "${BASEDIR}"/"${CATEGORY}"/ls.txt\n'
    # fmt:on

    mac_sh = UnixBashScript()
    cmds = mac_sh.write_script("", unix_content, mac_sh.write_checks_cmds)

    assert expected_output in cmds


def test_write_script_for_windows_powershell(windows_content):
    # fmt:off
    expected_output = '\n$category="a_category_with_space"\nWrite-Output "[*] Starting Collection commands of category: $category..."\nNew-Item -ItemType Directory -Force -Path $basedir\\$category | Out-Null\ndir > $basedir\\$category\\dir.txt\n'
    # fmt:on

    windows_ps1 = WindowsPowershellScript()
    cmds = windows_ps1.write_script("", windows_content, windows_ps1.write_checks_cmds)

    assert expected_output in cmds


def test_write_script_for_windows_powershell_cmdlet_1(
    windows_powershell_cmdlet_content_1,
):
    # fmt:off
    expected_output = '\n$category="a_category_with_space"\nWrite-Output "[*] Starting Collection commands of category: $category..."\nNew-Item -ItemType Directory -Force -Path $basedir\\$category | Out-Null\ndir | Out-File -Encoding utf8 -FilePath $basedir\\$category\\dir.txt\n'
    # fmt:on

    windows_ps1 = WindowsPowershellScript()
    cmds = windows_ps1.write_script(
        "", windows_powershell_cmdlet_content_1, windows_ps1.write_checks_cmds
    )

    assert expected_output in cmds


def test_write_script_for_windows_powershell_cmdlet_2(
    windows_powershell_cmdlet_content_2,
):
    # fmt:off
    expected_output = '\n$category="a_category_with_space"\nWrite-Output "[*] Starting Collection commands of category: $category..."\nNew-Item -ItemType Directory -Force -Path $basedir\\$category | Out-Null\ndir | Out-File -Encoding utf8 -Append -FilePath $basedir\\$category\\dir.txt\n'
    # fmt:on

    windows_ps1 = WindowsPowershellScript()
    cmds = windows_ps1.write_script(
        "", windows_powershell_cmdlet_content_2, windows_ps1.write_checks_cmds
    )

    assert expected_output in cmds


def test_write_script_for_windows_powershell_cmdlet_3(
    windows_powershell_cmdlet_content_3,
):
    # fmt:off
    expected_output = '\n$category="a_category_with_space"\nWrite-Output "[*] Starting Collection commands of category: $category..."\nNew-Item -ItemType Directory -Force -Path $basedir\\$category | Out-Null\ndir | Out-File -Append -Encoding utf8 -FilePath $basedir\\$category\\dir.txt\n'
    # fmt:on

    windows_ps1 = WindowsPowershellScript()
    cmds = windows_ps1.write_script(
        "", windows_powershell_cmdlet_content_3, windows_ps1.write_checks_cmds
    )

    assert expected_output in cmds


def test_write_checks_cmds_for_linux(unix_content):
    checkdir = "${CHECKSDIR}"
    expected_output = []
    expected_output.append('\necho "[*] Starting Compliance checks..."\n')
    expected_output.append('whoami >> "${CHECKSDIR}"/rule_id.txt\n')
    expected_output.append('\necho "[+] Finished Compliance checks."\n')

    output = UnixBashScript().write_checks_cmds(checkdir, unix_content, [])

    assert output == expected_output


def test_write_checks_cmds_for_mac(unix_content):
    checkdir = "${CHECKSDIR}"
    expected_output = []
    expected_output.append('\necho "[*] Starting Compliance checks..."\n')
    expected_output.append('whoami >> "${CHECKSDIR}"/rule_id.txt\n')
    expected_output.append('\necho "[+] Finished Compliance checks."\n')

    output = UnixBashScript().write_checks_cmds(checkdir, unix_content, [])

    assert output == expected_output


def test_write_checks_cmds_for_windows_powershell(windows_content):
    checkdir = "$checksdir"
    expected_output = []
    expected_output.append('\nWrite-Output "[*] Starting Compliance checks..."\n')
    expected_output.append(
        "whoami /all | Out-File -Encoding utf8 -Append -FilePath $checksdir\\rule_id.txt\n"
    )
    expected_output.append('\nWrite-Output "[+] Finished Compliance checks."\n')

    output = WindowsPowershellScript().write_checks_cmds(checkdir, windows_content, [])

    assert output == expected_output
