# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from octoconf.decorators.decorator import Decorator


class PowershellDecorator(Decorator):
    """
    It allows to add instructions before and after the execution of the commands. Among these instructions are the verification of the user's privileges, the creation of the working folder and the creation of the archive.
    """

    def decorator(func):
        def inner(*args, **kwargs):
            content = []
            prolog = """# Prolog
#Requires -RunAsAdministrator
#Requires -version 2

Write-Output "[*] Preparation..."
$basedir = "$pwd\Audit_$($env:COMPUTERNAME)_$(get-date -f yyyyMMdd-hhmmss)"
New-Item -ItemType directory -Path $basedir
$system_information_dir = "$basedir\\00_system_information"
New-Item -ItemType directory -Path $system_information_dir
$checksdir = "$basedir\\10_octoconf_checks"
New-Item -ItemType directory -Path $checksdir

date >> $system_information_dir\\timestamp.txt
systeminfo >> $system_information_dir\\systeminfo.txt

# Configuration collection
Write-Output "[*] Beginning of the collection..."
"""
            content.append(prolog)
            content.extend(func(*args, **kwargs))
            epilog = """# Epilog
Write-Output "[*] Finishing..."
date >> $system_information_dir\\timestamp.txt
try {
    Get-Command Compress-Archive | Out-Null
    Compress-Archive -Path ($basedir) -DestinationPath "$($basedir).zip"
    Write-Output "[+] Archive created!"
} catch {
    Write-Error "[x] Compress-Archive command not found!"
}
Write-Output "[+] Done!"
"""
            content.append(epilog)
            return content

        return inner
