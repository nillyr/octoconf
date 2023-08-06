# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import sys

sys.path.append("../../octoconf/")
from octoconf.interface_adapters.checker import CheckerInterfaceAdapter


def test_check_exact_case_insensitive():
    expected = "lower result"
    output = "LoWer ReSULT"
    assert True == CheckerInterfaceAdapter().check_exact(output, expected)


def test_check_exact_missing_output_value():
    expected = "a_result"
    output = ""
    assert False == CheckerInterfaceAdapter().check_exact(output, expected)


def test_check_exact_unix_return_carriage():
    expected = "a_result"
    output = "a_result\n"
    assert True == CheckerInterfaceAdapter().check_exact(output, expected)


def test_check_exact_windows_return_carriage():
    expected = "a_result"
    output = "a_result\r\n"
    assert True == CheckerInterfaceAdapter().check_exact(output, expected)


def test_check_regex_case_multiline():
    expected = ".*hibernatemode\\s+25.*"
    output = """
    System-wide power settings:
    Currently in use:
    standbydelaylow      blah
    standby              blah
    sleep                blah
    autopoweroffdelay    blah
    hibernatemode        25
    autopoweroff         blah
    ttyskeepawake        blah
    """

    assert True == CheckerInterfaceAdapter().check_regex(output, expected)


def test_check_regex_case_insentive_first():
    expected = ".*HIBERNATEMODE\\s+25.*"
    output = """
    System-wide power settings:
    Currently in use:
    standbydelaylow      blah
    standby              blah
    sleep                blah
    autopoweroffdelay    blah
    hibernatemode        25
    autopoweroff         blah
    ttyskeepawake        blah
    """

    assert True == CheckerInterfaceAdapter().check_regex(output, expected)


def test_check_regex_case_insentive_second():
    expected = ".*hibernatemode\\s+25.*"
    output = """
    System-wide power settings:
    Currently in use:
    standbydelaylow      blah
    standby              blah
    sleep                blah
    autopoweroffdelay    blah
    HIBERNATEMODE        25
    autopoweroff         blah
    ttyskeepawake        blah
    """

    assert True == CheckerInterfaceAdapter().check_regex(output, expected)
