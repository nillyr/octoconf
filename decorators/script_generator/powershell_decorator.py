from icecream import ic

from decorators.decorator import Decorator


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
$basedir = "$pwd\Audit_$env:COMPUTERNAME_$(get-date -f yyyyMMdd-hhmmss)"
New-Item -ItemType directory -Path $basedir
$checksdir = "$basedir\checks"
New-Item -ItemType directory -Path $checksdir

date >> $basedir\\timestamp.log

# Configuration collection
Write-Output "[*] Beginning of the collection..."
"""
            content.append(prolog)
            content.extend(func(*args, **kwargs))
            epilog = """# Epilog
Write-Output "[*] Finishing..."
date >> $basedir\\timestamp.log
Write-Output "[+] Done!"
"""
            content.append(epilog)
            return content

        return inner
