#!/bin/bash
if [ -d /mnt/TeslaCam/TeslaCam ] ; then
 echo "Drives are Mounted.... unmounting";
 umount /mnt/TeslaCam;
 umount /mnt/TeslaMusic;
 kpartx -d /piusb.bin;
 echo "Initiating Drives for use by Tesla. <BR>";
 modprobe g_mass_storage file=/piusb.bin ro=0 stale=0;
 echo 'Drives Mounted. Please check for Dashcam Icon.';
else
 echo "TeslaCam Already Mounted"
fi
