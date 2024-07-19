#!/bin/sh


echo "device" > /sys/bus/platform/devices/1c19400.phy/usb_role/1c19400.phy-role-switch/role

sleep 5

python read_cc.py 3
echo "OTG mode"
