#!/bin/bash

if ! [ -x "$(command -v python3)" ]; then
  echo '[x] python3 is not installed' >&2
  exit 1
else
  echo '[+] Found python3'
fi

python3 -m pip -V
if [ $? -eq 0 ]; then
  echo '[+] Found pip'
  echo '[*] Running pip upgrade...'
  python3 -m pip install --no-cache-dir --upgrade pip
else
  echo '[x] pip not found' >&2
  exit 1
fi

echo '[*] Creating a virtual environment...'
rm -rf ./venv
python3 -m venv venv
if [ $? -eq 0 ]; then
  source venv/bin/activate
  pip install --upgrade pip
else
  echo '[x] Failed to create virtual environment' >&2
  exit 1
fi

echo '[*] Installing the prerequisites...'
pip install --no-cache-dir -r requirements.txt
if [ $? -eq 0 ]; then
  echo '[+] Installation complete!'
else
  echo '[x] Installation failed' >&2
  exit 1
fi

exit 0
