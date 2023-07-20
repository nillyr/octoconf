#!/bin/bash

# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

if ! [ -x "$(command -v python3)" ]; then
  echo '[x] python3 is not installed' >&2
  exit 1
else
  echo '[+] Found python3'
  minor=$(python3 --version 2>&1 | awk "{print $2}" | cut -d'.' -f2)
  if [ "$minor" -lt "8" ]; then
    echo '[x] The minimum required version of python is python3.8' >&2
    exit 1
  fi
fi

if ! python3 -m pip -V; then
  echo '[x] pip not found' >&2
  exit 1
fi

echo '[+] Found pip'
echo '[*] Running pip upgrade...'
python3 -m pip install --no-cache-dir --upgrade pip

echo '[*] Creating a virtual environment...'
rm -rf ./venv
if ! python3 -m venv venv; then
  echo '[x] Failed to create a virtual environment' >&2
  exit 1
fi

# shellcheck source=/dev/null
source venv/bin/activate
pip install --upgrade pip
pip install setuptools wheel

echo '[*] Installing the prerequisites...'
if ! pip install --no-cache-dir -r requirements-dev.txt; then
  echo '[x] Installation failed' >&2
  exit 1
fi

echo '[+] Installation complete!'
exit 0
