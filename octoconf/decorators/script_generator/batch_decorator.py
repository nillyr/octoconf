# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoconf
# @since 1.0.0b

from octoconf.decorators.decorator import Decorator


class BatchDecorator(Decorator):
    """
    It allows to add instructions before and after the execution of the commands. Among these instructions are the verification of the user's privileges, the creation of the working folder and the creation of the archive.
    """

    def decorator(func):
        def inner(*args, **kwargs):
            content = []
            prolog = """REM Prolog

@@echo off
echo [*] Preparation...
set basedir=Audit_Windows_%COMPUTERNAME%
set checksdir=%basedir%\\checks
mkdir %basedir%
mkdir %checksdir%

echo %time% >> %basedir%\\timestamp.txt

REM Configuration collection
echo [*] Beginning of the collection...
"""
            content.append(prolog)
            content.extend(func(*args, **kwargs))
            epilog = """
REM Epilog
echo [*] Finishing...
echo %time% >> %basedir%\\timestamp.txt

echo [+] Done!
exit /b"""
            content.append(epilog)
            return content

        return inner
