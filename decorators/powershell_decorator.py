#!/usr/bin/env python

from decorators.decorator import Decorator


class PowershellDecorator(Decorator):
    def decorator(func):
        def inner(*args, **kwargs):
            content = []
            prolog = (
                """# %s

# Prolog
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
                % args[1][0]["copyright"]
            )
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
