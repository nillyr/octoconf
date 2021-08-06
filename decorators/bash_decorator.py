#!/usr/bin/env python

from decorators.decorator import Decorator


class BashDecorator(Decorator):
    def decorator(func):
        def inner(*args, **kwargs):
            content = []
            prolog = '''#!/bin/bash

# Prolog
echo \"[*] Permission check...\"
if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "This script must be run as root."
    exit
fi
echo \"[+] OK!\"

echo \"[*] Preparation...\"
BASEDIR=$(/usr/bin/mktemp -d)
echo `date` >> \"${BASEDIR}\"/timestamp.log
exec 2>/dev/null

# Configuration collection
echo \"[*] Beginning of the collection...\"'''
            content.append(prolog)
            content.extend(func(*args, **kwargs))
            epilog = '''
# Epilog
echo \"[*] Finishing...\"
echo `date` >> \"${BASEDIR}\"/timestamp.log
/usr/bin/tar zcf \"${BASEDIR##*/}\".tar.gz -C \"${BASEDIR}\" .
/bin/rm -rf \"${BASEDIR}\"
echo \"[+] Done!\"'''
            content.append(epilog)
            return content

        return inner
