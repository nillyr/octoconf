# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import sys

import pytest

sys.path.append("../../octoconf/")
from octoconf.interfaces.generate_script.windows_script import IWindowsScript


@pytest.fixture
def windows_basics_redirectors():
    return [
        "whoami > whoami.txt",
        "whoami >> whoami.txt",
        "whoami 1> whoami.txt",
        "whoami 3> whoami.txt",
        "whoami *> whoami.txt",
        "whoami 4>&1 > whoami.txt",
        "whoami 4>&1 >> whoami.txt",
        "whoami *>&1 > whoami.txt",
        "whoami *>&1 >> whoami.txt",
        '&{\nWrite-Warning "hello"\nWrite-Error "hello"\nWrite-Output "hello"\n} 3>&1 2>&1 > redirection.txt',
        'if ($a > $b) { "true" } elseif ( $c > $d ) { "true" } else { "false" } > comparison_operators.txt',
        '$(try{ Get-Content a_file.txt *> a_another_file.txt; Write-Output "hi" }catch{$Error[0]}) | Out-File -FilePath output.txt',
        '$(try{ Get-Content a_file.txt *> a_another_file.txt; if ($a > $b) { "true" } elseif ( $c > $d ) { "true" } else { "false" } } catch { $Error[0] }) | Out-File -FilePath output.txt',
    ]


@pytest.fixture
def windows_basics_redirectors_expected():
    return [
        "whoami > $basedir\\$category\\whoami.txt",
        "whoami >> $basedir\\$category\\whoami.txt",
        "whoami 1> $basedir\\$category\\whoami.txt",
        "whoami 3> $basedir\\$category\\whoami.txt",
        "whoami *> $basedir\\$category\\whoami.txt",
        "whoami 4>&1 > $basedir\\$category\\whoami.txt",
        "whoami 4>&1 >> $basedir\\$category\\whoami.txt",
        "whoami *>&1 > $basedir\\$category\\whoami.txt",
        "whoami *>&1 >> $basedir\\$category\\whoami.txt",
        '&{\nWrite-Warning "hello"\nWrite-Error "hello"\nWrite-Output "hello"\n} 3>&1 2>&1 > $basedir\\$category\\redirection.txt',
        'if ($a > $b) { "true" } elseif ( $c > $d ) { "true" } else { "false" } > $basedir\\$category\\comparison_operators.txt',
        '$(try{ Get-Content a_file.txt *> $basedir\\$category\\a_another_file.txt; Write-Output "hi" }catch{$Error[0]}) | Out-File -FilePath $basedir\\$category\\output.txt',
        '$(try{ Get-Content a_file.txt *> $basedir\\$category\\a_another_file.txt; if ($a > $b) { "true" } elseif ( $c > $d ) { "true" } else { "false" } } catch { $Error[0] }) | Out-File -FilePath $basedir\\$category\\output.txt',
    ]


def test_windows_basics_redirectors(
    windows_basics_redirectors, windows_basics_redirectors_expected
):
    output = []
    for cmd in windows_basics_redirectors:
        output.append(
            IWindowsScript.preprocess_collection_cmd("$basedir\\$category\\", cmd)
        )
    assert output == windows_basics_redirectors_expected


@pytest.fixture
def windows_cmd_gpresult_redirectors():
    return [
        "gpresult /H gpreport.html",
        "gpresult /Scope computer /H gpreport.html",
    ]


@pytest.fixture
def windows_cmd_gpresult_redirectors_expected():
    return [
        "gpresult /H $basedir\\$category\\gpreport.html",
        "gpresult /Scope computer /H $basedir\\$category\\gpreport.html",
    ]


def test_windows_cmd_gpresult_redirectors(
    windows_cmd_gpresult_redirectors, windows_cmd_gpresult_redirectors_expected
):
    output = []
    for cmd in windows_cmd_gpresult_redirectors:
        output.append(
            IWindowsScript.preprocess_collection_cmd("$basedir\\$category\\", cmd)
        )
    assert output == windows_cmd_gpresult_redirectors_expected


@pytest.fixture
def windows_cmd_secedit_redirectors():
    return [
        "secedit /export /cfg secedit.txt",
    ]


@pytest.fixture
def windows_cmd_secedit_redirectors_expected():
    return [
        "secedit /export /cfg $basedir\\$category\\secedit.txt",
    ]


def test_windows_cmd_secedit_redirectors(
    windows_cmd_secedit_redirectors, windows_cmd_secedit_redirectors_expected
):
    output = []
    for cmd in windows_cmd_secedit_redirectors:
        output.append(
            IWindowsScript.preprocess_collection_cmd("$basedir\\$category\\", cmd)
        )
    assert output == windows_cmd_secedit_redirectors_expected


@pytest.fixture
def windows_cmd_msinfo32_redirectors():
    return [
        "msinfo32.exe /report report.txt",
    ]


@pytest.fixture
def windows_cmd_msinfo32_redirectors_expected():
    return [
        "msinfo32.exe /report $basedir\\$category\\report.txt",
    ]


def test_windows_cmd_msinfo32_redirectors(
    windows_cmd_msinfo32_redirectors, windows_cmd_msinfo32_redirectors_expected
):
    output = []
    for cmd in windows_cmd_msinfo32_redirectors:
        output.append(
            IWindowsScript.preprocess_collection_cmd("$basedir\\$category\\", cmd)
        )
    assert output == windows_cmd_msinfo32_redirectors_expected


@pytest.fixture
def windows_cmdlet_export_csv_redirectors():
    return [
        "Get-Process -Name WmiPrvSE | Export-CSV -Path WmiData.csv -NoTypeInformation",
        "Get-Process -Name WmiPrvSE | Export-CSV -Encoding utf8 -Path WmiData.csv -NoTypeInformation",
    ]


@pytest.fixture
def windows_cmdlet_export_csv_redirectors_expected():
    return [
        "Get-Process -Name WmiPrvSE | Export-CSV -Path $basedir\\$category\\WmiData.csv -NoTypeInformation",
        "Get-Process -Name WmiPrvSE | Export-CSV -Encoding utf8 -Path $basedir\\$category\\WmiData.csv -NoTypeInformation",
    ]


def test_windows_cmdlet_export_csv_redirectors(
    windows_cmdlet_export_csv_redirectors,
    windows_cmdlet_export_csv_redirectors_expected,
):
    output = []
    for cmd in windows_cmdlet_export_csv_redirectors:
        output.append(
            IWindowsScript.preprocess_collection_cmd("$basedir\\$category\\", cmd)
        )
    assert output == windows_cmdlet_export_csv_redirectors_expected


@pytest.fixture
def windows_cmdlet_out_file_redirectors():
    return [
        "Get-Process -Name WmiPrvSE | ft -autosize -wrap | Out-File WmiPrvSE.txt",
        "Get-Process -Name WmiPrvSE | ft -autosize -wrap | Out-File -Encoding utf8 WmiPrvSE.txt",
        "Get-Process -Name WmiPrvSE | ft -autosize -wrap | Out-File -Encoding utf8 -FilePath WmiPrvSE.txt",
        "Get-Process -Name WmiPrvSE | ft -autosize -wrap | Out-File -Encoding utf8 -FilePath WmiPrvSE.txt -NoClobber",
        "Get-Process -Name WmiPrvSE | ft -autosize -wrap | Out-File -Encoding utf8 -Append -FilePath WmiPrvSE.txt",
    ]


@pytest.fixture
def windows_cmdlet_out_file_redirectors_expected():
    return [
        "Get-Process -Name WmiPrvSE | ft -autosize -wrap | Out-File $basedir\\$category\\WmiPrvSE.txt",
        "Get-Process -Name WmiPrvSE | ft -autosize -wrap | Out-File -Encoding utf8 $basedir\\$category\\WmiPrvSE.txt",
        "Get-Process -Name WmiPrvSE | ft -autosize -wrap | Out-File -Encoding utf8 -FilePath $basedir\\$category\\WmiPrvSE.txt",
        "Get-Process -Name WmiPrvSE | ft -autosize -wrap | Out-File -Encoding utf8 -FilePath $basedir\\$category\\WmiPrvSE.txt -NoClobber",
        "Get-Process -Name WmiPrvSE | ft -autosize -wrap | Out-File -Encoding utf8 -Append -FilePath $basedir\\$category\\WmiPrvSE.txt",
    ]


def test_windows_cmdlet_out_file_redirectors(
    windows_cmdlet_out_file_redirectors,
    windows_cmdlet_out_file_redirectors_expected,
):
    output = []
    for cmd in windows_cmdlet_out_file_redirectors:
        output.append(
            IWindowsScript.preprocess_collection_cmd("$basedir\\$category\\", cmd)
        )
    assert output == windows_cmdlet_out_file_redirectors_expected


@pytest.fixture
def windows_cmdlet_tee_object_redirectors():
    return [
        "Get-Process -Name WmiPrvSE | ft -autosize -wrap | Tee-Object WmiPrvSE.txt",
        "Get-Process -Name WmiPrvSE | ft -autosize -wrap | Tee-Object -Encoding utf8 WmiPrvSE.txt",
        "Get-Process -Name WmiPrvSE | ft -autosize -wrap | Tee-Object -Encoding utf8 -FilePath WmiPrvSE.txt",
        "Get-Process -Name WmiPrvSE | ft -autosize -wrap | Tee-Object -Encoding utf8 -FilePath WmiPrvSE.txt -Append",
    ]


@pytest.fixture
def windows_cmdlet_tee_object_redirectors_expected():
    return [
        "Get-Process -Name WmiPrvSE | ft -autosize -wrap | Tee-Object $basedir\\$category\\WmiPrvSE.txt",
        "Get-Process -Name WmiPrvSE | ft -autosize -wrap | Tee-Object -Encoding utf8 $basedir\\$category\\WmiPrvSE.txt",
        "Get-Process -Name WmiPrvSE | ft -autosize -wrap | Tee-Object -Encoding utf8 -FilePath $basedir\\$category\\WmiPrvSE.txt",
        "Get-Process -Name WmiPrvSE | ft -autosize -wrap | Tee-Object -Encoding utf8 -FilePath $basedir\\$category\\WmiPrvSE.txt -Append",
    ]


def test_windows_cmdlet_tee_object_redirectors(
    windows_cmdlet_tee_object_redirectors,
    windows_cmdlet_tee_object_redirectors_expected,
):
    output = []
    for cmd in windows_cmdlet_tee_object_redirectors:
        output.append(
            IWindowsScript.preprocess_collection_cmd("$basedir\\$category\\", cmd)
        )
    assert output == windows_cmdlet_tee_object_redirectors_expected
