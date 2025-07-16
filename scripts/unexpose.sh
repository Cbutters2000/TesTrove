#!/bin/bash
if [ -d /mnt/TeslaCam/TeslaCam ] ; then
 echo "Drives are already unmounted from the Tesla";
else
echo "Now Dismounting Drives from Tesla and making them accessible to Rpi. <BR>";
modprobe -r g_mass_storage;
sleep 4;
echo "Mounting Drives to Rpi </br>";
kpartx -a /piusb.bin;
sleep 2;
mount -o iocharset=utf8 -o loop /dev/mapper/loop0p1 /mnt/TeslaCam;
mount -o iocharset=utf8 -o loop /dev/mapper/loop0p2 /mnt/TeslaMusic;
echo "TeslaCam and TeslaMusic are now accessible to the Rpi."

fi
