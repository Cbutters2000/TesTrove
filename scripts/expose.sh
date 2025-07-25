#!/bin/bash
if [ -d /mnt/TeslaCam/TeslaCam ] ; then
 echo "Drives are Mounted.... unmounting";
 umount /mnt/TeslaCam;
 umount /mnt/TeslaMusic;
 kpartx -d /piusb.bin;
 echo "Initiating Drives for use by Tesla. <BR>";
 modprobe g_mass_storage file=/piusb.bin stale=0 removable=1;
 echo 'Drives Mounted. Please check for Dashcam Icon.';
else
 echo "TeslaCam Already Mounted"
fi
