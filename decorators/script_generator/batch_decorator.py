from decorators.decorator import Decorator


class BatchDecorator(Decorator):
    """
    It allows to add instructions before and after the execution of the commands. Among these instructions are the verification of the user's privileges, the creation of the working folder and the creation of the archive.
    """

    def decorator(func):
        def inner(*args, **kwargs):
            content = []
            prolog = """REM Prolog

@@echo off
echo [*] Permission check...
net sessions >nul 2>&1
if errorlevel 1 (
    echo This script must be run as an administrator.
    exit /b
)
echo [+] OK!

echo [*] Preparation...
set basedir=Audit_Windows_%COMPUTERNAME%
set checksdir=%basedir%\\checks
mkdir %basedir%
mkdir %checksdir%

echo %time% >> %basedir%\\timestamp.log

REM Configuration collection
echo [*] Beginning of the collection...
"""
            content.append(prolog)
            content.extend(func(*args, **kwargs))
            epilog = """
REM Epilog
echo [*] Finishing...
echo %time% >> %basedir%\\timestamp.log

echo [+] Done!
exit /b"""
            content.append(epilog)
            return content

        return inner
