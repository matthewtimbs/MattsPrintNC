#!/bin/bash

echo "Switching to Internet LAN connection - set switchbox to B"

wicd-cli --disconnect --wired

wicd-cli --load-profile "wiredonline" --wired

wicd-cli --connect  --wired

wicd-cli --status

