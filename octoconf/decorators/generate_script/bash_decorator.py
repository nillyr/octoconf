# @copyright Copyright (c) 2021 Nicolas GRELLETY
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
# shellcheck disable=SC2002

# Prevent overwriting of existing files
set -o noclobber

EXIT_STATUS=0

echo "[*] Starting Data collection..."

BASEDIR=$(mktemp -d -t tmp.XXXXXXXXXXXX)
CHECKSDIR="${BASEDIR}"/10_octoconf_checks

mkdir -p "${CHECKSDIR}"

date >> "${BASEDIR}"/date.txt"""
            content.append(prolog)
            content.extend(func(*args, **kwargs))
            epilog = """
date >> "${BASEDIR}"/date.txt

tar zcf "${HOSTNAME-$(hostname)}_$(date '+%Y%m%d-%H%M%S').tar.gz" -C "$BASEDIR" .
retval=$?
if [ "$retval" -eq 0 ]; then
    rm -rf "$BASEDIR"
    EXIT_STATUS=0
else
    echo "[x] Unable to create archive. ${BASEDIR} has not been deleted." >&2
    EXIT_STATUS=1
fi

echo "[+] Finished Data collection."

exit $EXIT_STATUS
"""
            content.append(epilog)
            return content

        return inner
