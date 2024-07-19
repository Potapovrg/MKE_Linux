#!/bin/sh

python read_cc.py 2
echo "host" > /sys/bus/platform/devices/1c19400.phy/usb_role/1c19400.phy-role-switch/role
echo "ADB mode"


