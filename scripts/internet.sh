#!/bin/bash

echo "Switching to Internet LAN connection - set switchbox to B"

nmcli con down "MESA CNC" "Internet Wired"
nmcli con up "Internet Wired"


