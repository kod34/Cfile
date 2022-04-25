#!/bin/bash
sudo apt install tor xterm -y
pip3 install -r requirements.txt 
echo -e "ControlPort 9051\nCookieAuthentication 0" > torrc
sudo cp $(readlink -f cfile.py) ${PATH%%:*}/cfile
