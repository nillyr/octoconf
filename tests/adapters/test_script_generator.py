import json
from adapters.script_generator.linux_bash_script import LinuxBashScript
from adapters.script_generator.macos_bash_script import MacOSBashScript
from adapters.script_generator.windows_batch_script import WindowsBatchScript
from adapters.script_generator.windows_powershell_script import WindowsPowershellScript


def test_write_checks_cmds_for_linux():
    checkdir = "${CHECKSDIR}"
    content = []
    content.append(
        {
            "category_id": 1,
            "checks_cmds": [["1.1.1", "whoami"], ["1.1.2", "id"]],
        }
    )
    cmds = []

    expected_output = []
    expected_output.append("\n# Checks\n")
    expected_output.append('whoami > "${CHECKSDIR}"/1.1.1.txt\n')
    expected_output.append('id > "${CHECKSDIR}"/1.1.2.txt\n')

    output = LinuxBashScript().write_checks_cmds(checkdir, content, cmds)

    assert output == expected_output


def test_write_checks_cmds_for_mac():
    checkdir = "${CHECKSDIR}"
    content = []
    content.append(
        {
            "category_id": 1,
            "checks_cmds": [["1.1.1", "whoami"], ["1.1.2", "id"]],
        }
    )
    cmds = []

    expected_output = []
    expected_output.append("\n# Checks\n")
    expected_output.append('whoami > "${CHECKSDIR}"/1.1.1.txt\n')
    expected_output.append('id > "${CHECKSDIR}"/1.1.2.txt\n')

    output = MacOSBashScript().write_checks_cmds(checkdir, content, cmds)

    assert output == expected_output


def test_write_checks_cmds_for_windows_batch():
    checkdir = "%checksdir%"
    content = []
    content.append(
        {
            "category_id": 1,
            "checks_cmds": [["1.1.1", "whoami /all"], ["1.1.2", "net users"]],
        }
    )
    cmds = []

    expected_output = []
    expected_output.append("\r\nREM Checks\r\n")
    expected_output.append("whoami /all > %checksdir%\\1.1.1.txt\r\n")
    expected_output.append("net users > %checksdir%\\1.1.2.txt\r\n")

    output = WindowsBatchScript().write_checks_cmds(checkdir, content, cmds)

    assert output == expected_output


def test_write_checks_cmds_for_windows_powershell():
    checkdir = "$checksdir"
    content = []
    content.append(
        {
            "category_id": 1,
            "checks_cmds": [["1.1.1", "whoami /all"], ["1.1.2", "net users"]],
        }
    )
    cmds = []

    expected_output = []
    expected_output.append("\r\n# Checks\r\n")
    expected_output.append("whoami /all | Out-File -Path $checksdir\\1.1.1.txt\r\n")
    expected_output.append("net users | Out-File -Path $checksdir\\1.1.2.txt\r\n")

    output = WindowsPowershellScript().write_checks_cmds(checkdir, content, cmds)

    assert output == expected_output
