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
            prolog = '''#!/bin/bash

if [[ ! "${EUID}" -eq 0 ]]; then
    echo "[x] This script must be run as 'root'"
    exit 1
fi

# Prolog
echo \"[*] Preparation...\"
BASEDIR="$(pwd)/audit_$(hostname)_$(date '+%Y%m%d-%H%M%S')"
mkdir -p \"${BASEDIR}\"
SYSTEMINFORMATIONDIR=\"${BASEDIR}\"/00_system_information
mkdir -p \"${SYSTEMINFORMATIONDIR}\"
CHECKSDIR=\"${BASEDIR}\"/10_octoconf_checks
mkdir -p \"${CHECKSDIR}\"

exec 2>\"${BASEDIR}\"/stderr.txt

# Standard system information
date >> \"${SYSTEMINFORMATIONDIR}\"/timestamp.txt
hostname -f > \"${SYSTEMINFORMATIONDIR}\"/hostname.txt
lsb_release -d | awk -F: '{print $2}' | sed -r "s/\\t+//g" > \"${SYSTEMINFORMATIONDIR}\"/os.txt
lsb_release -r | awk -F: '{print $2}' | sed -r "s/\\t+//g" > \"${SYSTEMINFORMATIONDIR}\"/os_version.txt
cat /etc/*ease* > \"${SYSTEMINFORMATIONDIR}\"/release.txt
uname -a > \"${SYSTEMINFORMATIONDIR}\"/system_information.txt
for keyword in system-manufacturer system-product-name bios-release-date bios-version; do echo "$keyword = " $(dmidecode -s $keyword) >> \"${SYSTEMINFORMATIONDIR}\"/smbios_information.txt; done
hostnamectl > \"${SYSTEMINFORMATIONDIR}\"/hostnamectl.txt
env > \"${SYSTEMINFORMATIONDIR}\"/env.txt
whoami > \"${SYSTEMINFORMATIONDIR}\"/whoami.txt
'''
            content.append(prolog)
            content.extend(func(*args, **kwargs))
            epilog = '''
# Epilog
echo \"[*] Finishing...\"
date >> \"${SYSTEMINFODIR}\"/timestamp.txt
tar zcf \"${BASEDIR##*/}\".tar.gz -C \"${BASEDIR}\" .
rm -rf \"${BASEDIR}\"
echo \"[+] Done!\"'''
            content.append(epilog)
            return content

        return inner
