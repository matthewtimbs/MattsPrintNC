#!/bin/bash

echo "Switching to Mesa CNC Controller LAN connection - set switchbox to A"

wicd-cli --disconnect --wired

wicd-cli --connect --network 3 --wired

wicd-cli --status


