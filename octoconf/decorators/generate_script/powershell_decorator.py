# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

from typing import Any

from octoconf.decorators.decorator import Decorator


class PowershellDecorator(Decorator):
    """
    It allows to add instructions before and after the execution of the commands. Among these instructions are the verification of the user's privileges, the creation of the working folder and the creation of the archive.
    """

    def decorator(func) -> Any:
        def inner(*args, **kwargs):
            content = []
            prolog = """#Requires -RunAsAdministrator
#Requires -version 2

$ExitCode = 0

# This function does nothing but return the data that has been received.
# We recommend to use a utility file with all the cryptographic operations.
Function Encrypt-Symetric() {
    Param(
        [Parameter(ValueFromPipeline=$true)] $UnencryptedString
    )

    Begin {}
    Process {
        return $UnencryptedString
    }
    End {}
}

if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Error "[x] Error: This script is meant to be run with administrator rights"
    $ExitCode = 1
    Exit($ExitCode)
}

Write-Output "[*] Starting Data collection..."

$basedir = "$pwd\\$($env:COMPUTERNAME)_$(Get-Date -f yyyyMMdd-hhmmss)"
$checksdir = "$basedir\\10_octoconf_checks"

New-Item -ItemType Directory -Force -Path $basedir | Out-Null
New-Item -ItemType Directory -Force -Path $checksdir | Out-Null

date >> $basedir\\timestamp.txt"""
            content.append(prolog)
            content.extend(func(*args, **kwargs))
            epilog = """
date >> $basedir\\timestamp.txt

try {
    Get-Command Compress-Archive | Out-Null
    Compress-Archive -Path ($basedir) -DestinationPath "$($basedir).zip"
    $ExitCode = 0
} catch {
    Write-Error "[x] Compress-Archive command not found!"
    $ExitCode = 1
}

Write-Output "[+] Finished Data collection."

Exit($ExitCode)
"""
            content.append(epilog)
            return content

        return inner
