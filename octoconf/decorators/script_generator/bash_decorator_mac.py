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

# Prolog
echo \"[*] Preparation...\"
BASEDIR=$(/usr/bin/mktemp -d)
CHECKSDIR=\"${BASEDIR}\"/checks
/bin/mkdir -p \"${CHECKSDIR}\"

/bin/date >> \"${BASEDIR}\"/timestamp.log

# Configuration collection
echo \"[*] Beginning of the collection...\"'''
            content.append(prolog)
            content.extend(func(*args, **kwargs))
            epilog = '''
# Epilog
echo \"[*] Finishing...\"
/bin/date >> \"${BASEDIR}\"/timestamp.log
/usr/bin/tar zcf \"${BASEDIR##*/}\".tar.gz -C \"${BASEDIR}\" .
/bin/rm -rf \"${BASEDIR}\"
echo \"[+] Done!\"'''
            content.append(epilog)
            return content

        return inner
