# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import sys

import pytest

sys.path.append("../octoconf/")
from octoconf.adapters.script_generator.linux_bash_script import LinuxBashScript
from octoconf.adapters.script_generator.macos_bash_script import MacOSBashScript
from octoconf.adapters.script_generator.windows_powershell_script import (
    WindowsPowershellScript,
)


@pytest.fixture
def unix_content():
    return [
        {
            "category_id": 1,
            "category_name": "a category with space",
            "checks_cmds": [["1.1.1", "whoami"], ["1.1.2", "id"]],
            "collection_cmds": ["ls -al > ls.txt"],
        }
    ]


@pytest.fixture
def windows_content():
    return [
        {
            "category_id": 1,
            "category_name": "a category with space",
            "checks_cmds": [["1.1.1", "whoami /all"], ["1.1.2", "net users"]],
            "collection_cmds": ["dir > dir.txt"],
        }
    ]


@pytest.fixture
def windows_powershell_cmdlet_content_1():
    return [
        {
            "category_id": 1,
            "category_name": "a category with space",
            "checks_cmds": [["1.1.1", "whoami /all"], ["1.1.2", "net users"]],
            "collection_cmds": ["dir | Out-File -Encoding utf8 -FilePath dir.txt"],
        }
    ]


@pytest.fixture
def windows_powershell_cmdlet_content_2():
    return [
        {
            "category_id": 1,
            "category_name": "a category with space",
            "checks_cmds": [["1.1.1", "whoami /all"], ["1.1.2", "net users"]],
            "collection_cmds": [
                "dir | Out-File -Encoding utf8 -Append -FilePath dir.txt"
            ],
        }
    ]


@pytest.fixture
def windows_powershell_cmdlet_content_3():
    return [
        {
            "category_id": 1,
            "category_name": "a category with space",
            "checks_cmds": [["1.1.1", "whoami /all"], ["1.1.2", "net users"]],
            "collection_cmds": [
                "dir | Out-File -Encoding utf8 -Append -FilePath dir.txt"
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
    expected_output = '\nCATEGORY="a_category_with_space"\necho "[*] Running \\"${CATEGORY}\\" collection commands..."\n/bin/mkdir -p "${BASEDIR}"/"${CATEGORY}"/\nls -al >> "${BASEDIR}"/"${CATEGORY}"/ls.txt\n'
    # fmt:on

    linux_sh = LinuxBashScript()
    cmds = linux_sh.write_script(unix_content, linux_sh.write_checks_cmds)

    assert expected_output in cmds


def test_write_script_for_mac(unix_content):
    # fmt:off
    expected_output = '\nCATEGORY="a_category_with_space"\necho "[*] Running \\"${CATEGORY}\\" collection commands..."\n/bin/mkdir -p "${BASEDIR}"/"${CATEGORY}"/\nls -al >> "${BASEDIR}"/"${CATEGORY}"/ls.txt\n'
    # fmt:on

    mac_sh = MacOSBashScript()
    cmds = mac_sh.write_script(unix_content, mac_sh.write_checks_cmds)

    assert expected_output in cmds


def test_write_script_for_windows_powershell(windows_content):
    # fmt:off
    expected_output = '\n$category="a_category_with_space"\nWrite-Output "[*] Running $category collection commands..."\nNew-Item -ItemType directory -Path $basedir\\$category\ndir > $basedir\\$category\\dir.txt\r\n'
    # fmt:on

    windows_ps1 = WindowsPowershellScript()
    cmds = windows_ps1.write_script(windows_content, windows_ps1.write_checks_cmds)

    assert expected_output in cmds


def test_write_script_for_windows_powershell_cmdlet_1(
    windows_powershell_cmdlet_content_1,
):
    # fmt:off
    expected_output = '\n$category="a_category_with_space"\nWrite-Output "[*] Running $category collection commands..."\nNew-Item -ItemType directory -Path $basedir\\$category\ndir | Out-File -Encoding utf8 -FilePath $basedir\\$category\\dir.txt\r\n'
    # fmt:on

    windows_ps1 = WindowsPowershellScript()
    cmds = windows_ps1.write_script(
        windows_powershell_cmdlet_content_1, windows_ps1.write_checks_cmds
    )

    assert expected_output in cmds


def test_write_script_for_windows_powershell_cmdlet_2(
    windows_powershell_cmdlet_content_2,
):
    # fmt:off
    expected_output = '\n$category="a_category_with_space"\nWrite-Output "[*] Running $category collection commands..."\nNew-Item -ItemType directory -Path $basedir\\$category\ndir | Out-File -Encoding utf8 -Append -FilePath $basedir\\$category\\dir.txt\r\n'
    # fmt:on

    windows_ps1 = WindowsPowershellScript()
    cmds = windows_ps1.write_script(
        windows_powershell_cmdlet_content_2, windows_ps1.write_checks_cmds
    )

    assert expected_output in cmds


def test_write_script_for_windows_powershell_cmdlet_3(
    windows_powershell_cmdlet_content_3,
):
    # fmt:off
    expected_output = '\n$category="a_category_with_space"\nWrite-Output "[*] Running $category collection commands..."\nNew-Item -ItemType directory -Path $basedir\\$category\ndir | Out-File -Encoding utf8 -Append -FilePath $basedir\\$category\\dir.txt\r\n'
    # fmt:on

    windows_ps1 = WindowsPowershellScript()
    cmds = windows_ps1.write_script(
        windows_powershell_cmdlet_content_3, windows_ps1.write_checks_cmds
    )

    assert expected_output in cmds


def test_write_checks_cmds_for_linux(unix_content):
    checkdir = "${CHECKSDIR}"
    expected_output = []
    expected_output.append("\n# Checks\n")
    expected_output.append('whoami >> "${CHECKSDIR}"/1.1.1.txt\n')
    expected_output.append('id >> "${CHECKSDIR}"/1.1.2.txt\n')

    output = LinuxBashScript().write_checks_cmds(checkdir, unix_content, [])

    assert output == expected_output


def test_write_checks_cmds_for_mac(unix_content):
    checkdir = "${CHECKSDIR}"
    expected_output = []
    expected_output.append("\n# Checks\n")
    expected_output.append('whoami >> "${CHECKSDIR}"/1.1.1.txt\n')
    expected_output.append('id >> "${CHECKSDIR}"/1.1.2.txt\n')

    output = MacOSBashScript().write_checks_cmds(checkdir, unix_content, [])

    assert output == expected_output


def test_write_checks_cmds_for_windows_powershell(windows_content):
    checkdir = "$checksdir"
    expected_output = []
    expected_output.append("\r\n# Checks\r\n")
    expected_output.append(
        "whoami /all | Out-File -Encoding utf8 -Append -FilePath $checksdir\\1.1.1.txt\r\n"
    )
    expected_output.append(
        "net users | Out-File -Encoding utf8 -Append -FilePath $checksdir\\1.1.2.txt\r\n"
    )

    output = WindowsPowershellScript().write_checks_cmds(checkdir, windows_content, [])

    assert output == expected_output


def test_write_check_with_collect_only_and_not_only_powershell(
    collect_only_and_not_only,
):
    # fmt:off
    expected_output = '\n$category="a_category_with_space"\nWrite-Output "[*] Running $category collection commands..."\nNew-Item -ItemType directory -Path $basedir\\$category\ndir > $basedir\\$category\\dir.txt\r\n'
    # fmt:on

    windows_ps1 = WindowsPowershellScript()
    cmds = windows_ps1.write_script(
        collect_only_and_not_only, windows_ps1.write_checks_cmds
    )

    expected_absent_check_cmd = (
        " | Out-File -Encoding utf8 -Append -FilePath $checksdir\\1.1.1.txt\r\n"
    )
    expected_check_cmd = "whoami /all | Out-File -Encoding utf8 -Append -FilePath $checksdir\\2.1.1.txt\r\n"

    assert expected_output in cmds
    assert expected_absent_check_cmd not in cmds
    assert expected_check_cmd in cmds


def test_write_check_with_collect_only_and_not_only_linux(collect_only_and_not_only):
    # fmt:off
    expected_output = '\nCATEGORY="a_category_with_space"\necho "[*] Running \\"${CATEGORY}\\" collection commands..."\n/bin/mkdir -p "${BASEDIR}"/"${CATEGORY}"/\ndir >> "${BASEDIR}"/"${CATEGORY}"/dir.txt\n'
    # fmt:on

    linux_sh = LinuxBashScript()
    cmds = linux_sh.write_script(collect_only_and_not_only, linux_sh.write_checks_cmds)

    expected_absent_check_cmd = ' >> "${CHECKSDIR}"/1.1.1.txt\n'
    expected_check_cmd = 'whoami /all >> "${CHECKSDIR}"/2.1.1.txt\n'

    assert expected_output in cmds
    assert expected_absent_check_cmd not in cmds
    assert expected_check_cmd in cmds


def test_write_check_with_collect_only_and_not_only_mac(collect_only_and_not_only):
    # fmt:off
    expected_output = '\nCATEGORY="a_category_with_space"\necho "[*] Running \\"${CATEGORY}\\" collection commands..."\n/bin/mkdir -p "${BASEDIR}"/"${CATEGORY}"/\ndir >> "${BASEDIR}"/"${CATEGORY}"/dir.txt\n'
    # fmt:on

    mac_sh = MacOSBashScript()
    cmds = mac_sh.write_script(collect_only_and_not_only, mac_sh.write_checks_cmds)

    expected_absent_check_cmd = ' >> "${CHECKSDIR}"/1.1.1.txt\n'
    expected_check_cmd = 'whoami /all >> "${CHECKSDIR}"/2.1.1.txt\n'

    assert expected_output in cmds
    assert expected_absent_check_cmd not in cmds
    assert expected_check_cmd in cmds
