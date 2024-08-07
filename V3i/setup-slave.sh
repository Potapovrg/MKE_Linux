#!/bin/sh

modprobe libcomposite
mount -t configfs none /sys/kernel/config
cd /sys/kernel/config/usb_gadget

mkdir g
cd g

echo 0x1d6b > idVendor # Linux Foundation
echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2
mkdir -p strings/0x409
echo "00001" > strings/0x409/serialnumber
echo "Zavdimka" > strings/0x409/manufacturer
echo "zavdimka USB Device" > strings/0x409/product
mkdir -p configs/c.1/strings/0x409
echo "Config 1: ECM network" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower

# Add Keyboard hidg0
mkdir -p functions/hid.keyboard
echo 1 > functions/hid.keyboard/protocol
echo 1 > functions/hid.keyboard/subclass
echo 8 > functions/hid.keyboard/report_length
echo 0 > functions/hid.keyboard/no_out_endpoint
echo -ne \\x05\\x01\\x09\\x06\\xa1\\x01\\x05\\x07\\x19\\xe0\\x29\\xe7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x05\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x05\\x91\\x02\\x95\\x01\\x75\\x03\\x91\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\x65\\x05\\x07\\x19\\x00\\x29\\x65\\x81\\x00\\xc0 > functions/hid.keyboard/report_desc
ln -s functions/hid.keyboard configs/c.1

#Add Mouse hidg1
mkdir -p functions/hid.mouse
echo 0 > functions/hid.mouse/protocol
echo 0 > functions/hid.mouse/subclass
echo 4 > functions/hid.mouse/report_length
echo 0 > functions/hid.mouse/no_out_endpoint
echo -ne \\x05\\x01\\x09\\x02\\xA1\\x01\\x09\\x01\\xA1\\x00\\x05\\x09\\x19\\x01\\x29\\x03\\x15\\x00\\x25\\x01\\x95\\x03\\x75\\x01\\x81\\x02\\x95\\x01\\x75\\x05\\x81\\x01\\x05\\x01\\x09\\x30\\x09\\x31\\x09\\x38\\x15\\x81\\x25\\x7F\\x75\\x08\\x95\\x03\\x81\\x06\\xC0\\x09\\x3c\\x05\\xff\\x09\\x01\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x02\\xb1\\x22\\x75\\x06\\x95\\x01\\xb1\\x01\\xc0 > functions/hid.mouse/report_desc
ln -s functions/hid.mouse configs/c.1

mkdir -p functions/ecm.usb0
echo  "C0:EA:C3:61:09:78" > functions/ecm.usb0/host_addr
echo  "C0:EA:C3:61:09:79" > functions/ecm.usb0/dev_addr
ln -s functions/ecm.usb0 configs/c.1

ls /sys/class/udc > UDC

chmod 777 /dev/hidg0
chmod 777 /dev/hidg1

sleep 3
ifup usb0
sleep 1
/etc/init.d/S80dnsmasq start
iptables -t nat -s 192.168.11.0/24 -A POSTROUTING -j MASQUERADE
iptables -t nat -A POSTROUTING -j MASQUERADE
echo 1 > /proc/sys/net/ipv4/ip_forward


