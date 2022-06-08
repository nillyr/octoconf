# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from octoconf.decorators.decorator import Decorator


class BashDecoratorMAC(Decorator):
    """
    It allows to add instructions before and after the execution of the commands. Among these instructions are the verification of the user's privileges, the creation of the working folder and the creation of the archive.
    """

    def decorator(func):
        def inner(*args, **kwargs):
            content = []
            prolog = '''#!/bin/bash

id -Gn $USER | grep -q -w admin
if [ $? -ne 0 ]; then
  echo "[x] You must be in the admin group to run this script."
  exit
fi

# Prolog
echo \"[*] Preparation...\"
BASEDIR="$(pwd)/audit_$(hostname)_$(date '+%Y%m%d-%H%M%S')"
mkdir -p \"${BASEDIR}\"
METADATADIR=\"${BASEDIR}\"/00_Metadata
mkdir -p \"${METADATADIR}\"
CHECKSDIR=\"${BASEDIR}\"/10_Checks
mkdir -p \"${CHECKSDIR}\"

exec 2>\"${BASEDIR}\"/stderr.txt

# Standard system information
date >> \"${METADATADIR}\"/timestamp.txt
system_profiler > \"${METADATADIR}\"/system_profiler.txt
uname -a > \"${METADATADIR}\"/system_information.txt
env > \"${METADATADIR}\"/env.txt

# Configuration collection
echo \"[*] Beginning of the collection...\"'''
            content.append(prolog)
            content.extend(func(*args, **kwargs))
            epilog = '''
# Epilog
echo \"[*] Finishing...\"
date >> \"${METADATADIR}\"/timestamp.txt
tar zcf \"${BASEDIR##*/}\".tar.gz -C \"${BASEDIR}\" .
rm -rf \"${BASEDIR}\"
echo \"[+] Done!\"'''
            content.append(epilog)
            return content

        return inner
