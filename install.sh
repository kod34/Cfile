#!/bin/bash
sudo apt install tor xterm -y
echo -e "ControlPort 9051\nCookieAuthentication 0" > torrc
