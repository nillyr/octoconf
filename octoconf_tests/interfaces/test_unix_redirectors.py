# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import sys

import pytest

sys.path.append("../../octoconf/")
from octoconf.interfaces.generate_script.unix_script import IUnixScript


@pytest.fixture
def unix_basics_redirectors():
    return [
        "id>id.txt",
        "id> id.txt",
        "id >id.txt",
        "id > id.txt",
        "id >| id.txt",
        "id>>id.txt",
        "id>> id.txt",
        "id >>id.txt",
        "id >> id.txt",
        "id1>id.txt",
        "id1> id.txt",
        "id 1>id.txt",
        "id 1> id.txt",
        "id1>>id.txt",
        "id1>> id.txt",
        "id 1>>id.txt",
        "id 1>> id.txt",
        "id&>id.txt",
        "id&> id.txt",
        "id &>id.txt",
        "id &> id.txt",
        "id 2>&1 > id.txt",
        "id 2>/dev/null > id.txt",
        "id 2>log_stderr.txt >|id.txt",
        "cat << EOF>here_document.txt\ndummy line 1\ndummy line 2\nEOF",
        "cat << EOF> here_document.txt\ndummy line 1\ndummy line 2\nEOF",
        "cat << EOF >here_document.txt\ndummy line 1\ndummy line 2\nEOF",
        "cat << EOF > here_document.txt\ndummy line 1\ndummy line 2\nEOF",
        "cat << EOF>>here_document.txt\ndummy line 1\ndummy line 2\nEOF",
        "cat << EOF>> here_document.txt\ndummy line 1\ndummy line 2\nEOF",
        "cat << EOF >>here_document.txt\ndummy line 1\ndummy line 2\nEOF",
        "cat << EOF >> here_document.txt\ndummy line 1\ndummy line 2\nEOF",
        "cat <<- EOF>here_document.txt\ndummy line 1\ndummy line 2\nEOF",
        "cat <<- EOF> here_document.txt\ndummy line 1\ndummy line 2\nEOF",
        "cat <<- EOF >here_document.txt\ndummy line 1\ndummy line 2\nEOF",
        "cat <<- EOF > here_document.txt\ndummy line 1\ndummy line 2\nEOF",
        'if (( $a > $b )); then echo "true" > comparison_operators.txt; fi',
        "(echo $(whoami |tee whoami.txt); id > id.txt; )",
        'id > id.txt; if (( 42 > 24 )); then echo "true" > comp.txt; fi',
    ]


@pytest.fixture
def unix_basics_redirectors_expected():
    return [
        'id>"${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id> "${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id >"${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id > "${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id >| "${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id>>"${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id>> "${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id >>"${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id >> "${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id1>"${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id1> "${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id 1>"${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id 1> "${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id1>>"${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id1>> "${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id 1>>"${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id 1>> "${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id&>"${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id&> "${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id &>"${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id &> "${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id 2>&1 > "${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id 2>/dev/null > "${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id 2>"${BASEDIR}"/"${CATEGORY}"/log_stderr.txt >|"${BASEDIR}"/"${CATEGORY}"/id.txt',
        'cat << EOF>"${BASEDIR}"/"${CATEGORY}"/here_document.txt\ndummy line 1\ndummy line 2\nEOF',
        'cat << EOF> "${BASEDIR}"/"${CATEGORY}"/here_document.txt\ndummy line 1\ndummy line 2\nEOF',
        'cat << EOF >"${BASEDIR}"/"${CATEGORY}"/here_document.txt\ndummy line 1\ndummy line 2\nEOF',
        'cat << EOF > "${BASEDIR}"/"${CATEGORY}"/here_document.txt\ndummy line 1\ndummy line 2\nEOF',
        'cat << EOF>>"${BASEDIR}"/"${CATEGORY}"/here_document.txt\ndummy line 1\ndummy line 2\nEOF',
        'cat << EOF>> "${BASEDIR}"/"${CATEGORY}"/here_document.txt\ndummy line 1\ndummy line 2\nEOF',
        'cat << EOF >>"${BASEDIR}"/"${CATEGORY}"/here_document.txt\ndummy line 1\ndummy line 2\nEOF',
        'cat << EOF >> "${BASEDIR}"/"${CATEGORY}"/here_document.txt\ndummy line 1\ndummy line 2\nEOF',
        'cat <<- EOF>"${BASEDIR}"/"${CATEGORY}"/here_document.txt\ndummy line 1\ndummy line 2\nEOF',
        'cat <<- EOF> "${BASEDIR}"/"${CATEGORY}"/here_document.txt\ndummy line 1\ndummy line 2\nEOF',
        'cat <<- EOF >"${BASEDIR}"/"${CATEGORY}"/here_document.txt\ndummy line 1\ndummy line 2\nEOF',
        'cat <<- EOF > "${BASEDIR}"/"${CATEGORY}"/here_document.txt\ndummy line 1\ndummy line 2\nEOF',
        'if (( $a > $b )); then echo "true" > "${BASEDIR}"/"${CATEGORY}"/comparison_operators.txt; fi',
        '(echo $(whoami |tee "${BASEDIR}"/"${CATEGORY}"/whoami.txt); id > "${BASEDIR}"/"${CATEGORY}"/id.txt; )',
        'id > "${BASEDIR}"/"${CATEGORY}"/id.txt; if (( 42 > 24 )); then echo "true" > "${BASEDIR}"/"${CATEGORY}"/comp.txt; fi',
    ]


def test_unix_basics_redirectors(
    unix_basics_redirectors, unix_basics_redirectors_expected
):
    output = []
    for cmd in unix_basics_redirectors:
        output.append(
            IUnixScript.preprocess_collection_cmd('"${BASEDIR}"/"${CATEGORY}"/', cmd)
        )
    assert output == unix_basics_redirectors_expected


@pytest.fixture
def unix_fd_to_files_redirectors():
    return [
        "exec 3>fd_to_file.txt\nid >&3\nexec 3>&-",
        "echo 1234567890 > file.txt\nexec 3<>file.txt\nread -rn 4 <&3\necho -n . >&3\nexec 3>&-",
    ]


@pytest.fixture
def unix_fd_to_files_redirectors_expected():
    return [
        'exec 3>"${BASEDIR}"/"${CATEGORY}"/fd_to_file.txt\nid >&3\nexec 3>&-',
        'echo 1234567890 > "${BASEDIR}"/"${CATEGORY}"/file.txt\nexec 3<>"${BASEDIR}"/"${CATEGORY}"/file.txt\nread -rn 4 <&3\necho -n . >&3\nexec 3>&-',
    ]


def test_unix_fd_to_files_redirectors(
    unix_fd_to_files_redirectors, unix_fd_to_files_redirectors_expected
):
    output = []
    for cmd in unix_fd_to_files_redirectors:
        output.append(
            IUnixScript.preprocess_collection_cmd('"${BASEDIR}"/"${CATEGORY}"/', cmd)
        )
    assert output == unix_fd_to_files_redirectors_expected


@pytest.fixture
def unix_tee_cmd_redirectors():
    return [
        "id | tee id.txt",
        "id | tee -a id.txt",
        "id | tee -i id.txt",
        "id | tee -i -a id.txt",
        "id | tee -p id.txt",
        "id | tee -p -i id.txt",
        "id | tee -p -i -a id.txt",
    ]


@pytest.fixture
def unix_tee_cmd_redirectors_expected():
    return [
        'id | tee "${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id | tee -a "${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id | tee -i "${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id | tee -i -a "${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id | tee -p "${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id | tee -p -i "${BASEDIR}"/"${CATEGORY}"/id.txt',
        'id | tee -p -i -a "${BASEDIR}"/"${CATEGORY}"/id.txt',
    ]


def test_unix_tee_cmd_redirectors(
    unix_tee_cmd_redirectors, unix_tee_cmd_redirectors_expected
):
    output = []
    for cmd in unix_tee_cmd_redirectors:
        output.append(
            IUnixScript.preprocess_collection_cmd('"${BASEDIR}"/"${CATEGORY}"/', cmd)
        )
    assert output == unix_tee_cmd_redirectors_expected
