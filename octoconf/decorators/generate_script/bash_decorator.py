# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from octoconf.decorators.decorator import Decorator


class BashDecorator(Decorator):
    """
    It allows to add instructions before and after the execution of the commands. Among these instructions are the verification of the user's privileges, the creation of the working folder and the creation of the archive.
    """

    def decorator(func):
        def inner(*args, **kwargs):
            content = []
            prolog = """#!/bin/bash

# Redirect /dev/stderr file descriptor
exec 2>\"${BASEDIR}\"/stderr.txt

# FIXME: à tester et compléter avec la gestion du chiffrement
save_to_file() {
    output_file=$1
    IFS=$'\\n' read -d "" -rs data_in <<< "$(cat /dev/stdin)"
    echo "$data_in" > "$output_file"
}

if [[ ! "${EUID}" -eq 0 ]]; then
    echo "[x] This script must be run as 'root'"
    exit 1
fi

BASEDIR="$(pwd)/audit_$(hostname)_$(date '+%Y%m%d-%H%M%S')"
CHECKSDIR=\"${BASEDIR}\"/10_octoconf_checks

mkdir -p \"${BASEDIR}\" \"${CHECKSDIR}\"

date >> \"${BASEDIR}\"/timestamp.txt
"""
            content.append(prolog)
            content.extend(func(*args, **kwargs))
            epilog = '''
echo \"[*] Finishing...\"
date >> \"${BASEDIR}\"/timestamp.txt
tar zcf \"${BASEDIR##*/}\".tar.gz -C \"${BASEDIR}\" .
rm -rf \"${BASEDIR}\"
echo \"[+] Done!\"'''
            content.append(epilog)
            return content

        return inner
