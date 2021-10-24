from decorators.decorator import Decorator


class BashDecoratorMAC(Decorator):
    """
    It allows to add instructions before and after the execution of the commands. Among these instructions are the verification of the user's privileges, the creation of the working folder and the creation of the archive.
    """

    def decorator(func):
        def inner(*args, **kwargs):
            content = []
            prolog = '''#!/bin/bash

# Prolog
echo \"[*] Permission check...\"
/usr/bin/id -Gn $USER | /usr/bin/grep -q -w admin
if [ $? -ne 0 ]; then
    echo "You must be in the admin group to run this script."
    exit
fi
echo \"[+] OK!\"

echo \"[*] Preparation...\"
BASEDIR=$(/usr/bin/mktemp -d)
CHECKSDIR=\"${BASEDIR}\"/checks
/usr/bin/mkdir -p \"${CHECKSDIR}\"

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
