# TesTrove -WIP DO NOT USE YET
TesTrove lets you use a Raspberry Pi Zero 2W to act as a storage device for your Tesla's Music and Dashcam &amp; enables cool syncing features.

## Initial Setup of SD card and Raspberry Pi Zero 2W:
This Guide helps you setup your Pi Zero with a volume that will have two partitions that it will use to act as a storage device over USB to share to your Tesla for Dashcam & Music Purposes. 

### FLASH OS ONTO SD CARD

Write MicroSD with Raspberry Pi OS Lite (Bookworm).

During setup, ensure these settings are configured:

- Set hostname: `teslasync` (or anyhostname you wish.)
- Set username and password.
- Configure Wi-Fi settings (SSID/Password).
  - Enable SSH during setup (recommended).

After boot, wait for reboots (2–3 total) while it completes initialization. If Wi-Fi fails to connect initially:
1. Connect a keyboard and monitor.
2. Run:
   ```bash
   sudo raspi-config
   ```
3. Navigate to **Option 5: Setup the WLAN Country** → Select your country.
4. Go back to **Option 1: S1 Wireless LAN** → Enter SSID/password.

Once Wi-Fi works, disconnect peripherals and SSH over the network from a different machine into the Raspberry Pi using your own credentials. For example:
```bash
ssh pi@[Pi-IP-Address]
```

---

## EDIT RPI ENVIRONMENT CONFIG FILES

### Edit `config.txt`
Edit `/boot/firmware/config.txt` using `sudo nano /boot/firmware/config.txt` if the line doesn’t exist in the [all] section; Add:

```bash
dtoverlay=dwc2
```
*(This ensures USB storage drivers load correctly.)*

### Edit `cmdline.txt`
Edit `/boot/firmware/cmdline.txt` using `sudo nano /boot/firmware/cmdline.txt`  (add the edit after the word `rootwait` on the same line):

```bash
modules-load=dwc2,g_mass_storage
```

### Update `/etc/modules` using 
```bash
sudo nano /etc/modules
```
Add the line:

```bash
dwc2
```

**Reboot** after making these changes.

---

## MAKE THE CONTAINER FILE

Run this command to pre-allocate space for your USB drive 
Make the bin size something much less than the size of your sd card. For example, for a 128GB card, only use 90GB, for a 256GB card only use 200GB. The command is:

Slow Method (I'm only including this here because many other tutorials do it this way)(adjust `count=32768` as needed for larger SD cards)
```bash
sudo dd bs=1M if=/dev/zero of=/piusb.bin count=32768 status=progress  # 32GB = 32768 × 1MB
```
*Note: This step may take hours and hours depending on the size of bin you are making.*

Fast Method (My preffered way to do this as it will create the file almost instantly.)
```bash
sudo fallocate -l 16G /piusb.bin  # Change 16GB to your desired size
```
## MAKE SOME MOUNT POINTS

Create directories for storage partitions:

```bash
sudo mkdir /mnt/TeslaCam     # Will act as a mount point for DashCam partition
sudo mkdir /mnt/TeslaMusic   # Will act as a mount point for Music partition
```
Let's also install an important program for interacting with these mount points later on.
```bash
sudo apt-get install kpartx
```

## USAGE COMMANDS FOR STORAGE DEVICE

### Activate USB Storage
Attach the Pi Zero to a Windows PC. !!BE SURE TO USE THE 2nd microUSB port which supports data AND power.!! We can now activate the storage so it appears as a drive for the windows machine, (just like it will when it is plugged into your tesla later.

## Presenting and Removing the Storage over USB:

To Present the storage:

```bash
sudo modprobe g_mass_storage file=/piusb.bin stall=0 removable=1
```
You should be able to hear the drive appearing on the USB on your windows machine.

To Remove the storage:

```bash
sudo modprobe -r g_mass_storage
```

You can try toggling these commands to make sure it works at this point, Success means you can see the volume in windows. Make sure your volume is seen and connected in order to do the next step.list disk

# FORMAT THE DRIVE INTO MULTIPLE PARTITIONS USING WINDOWS.
once you can see the drive in windows when the raspberry pi zero is plugged into it.
You may have to use the computer management window to see the volume. (run compmgmt.msc)
We will now create 2 partitions. The first partition will be for Music, The second partition will be for Dashcam Purposes.
**BE CAREFUL YOU SELECT THE CORRECT DISKS AS YOU COULD EASILY WIPE YOUR COMPUTER'S INFORMATION WITH THIS TOOL!**
Use **DiskPart** (Windows Command Prompt) :

1. Run Diskpart: `diskpart`
2.  View your volumes `list disk`.
3. Select target disk: `select disk [number]` (replace `[number]` with the volume the rpi is presenting windows).
4. Create the 1st partition Create the first partition. I recommend doing this one smaller than the dashcam partition. **in this example 8192 = 8GB**.
   - 1st partition (for Music) 
     ```powershell
     create partition primary size=8192
     ```
   - Format as exfat).
     ```powershell
     list partition  # Confirm partitions
     select partition 1  # Select Music partition
     format fs=exfat quick
     ```
5. Create the 2nd partition (For Dashcam) **Don't specify a size for the 2nd partition and it will use the remaining space**
   - 1st partition (for Music) 
     ```powershell
     create partition primary # Note we're not specifying a size on this one so it uses the rest of the volume.
     ```
   - Format as exfat).
     ```powershell
     list partition  # Confirm partitions
     select partition 2  # Select Dashcam partition
     format fs=exfat quick
     ```
You've now created your partitions!
1. Assign the partitions to a drive letter. I like to rename them for example TeslaMusic (D:) & TeslaCam (E:) 
2. Create a folder called "TeslaCam" inside the 2nd partition, as it is necessary to make it be recognized as the dashcam volume.

## MAKE THE STORAGE PRESENT ITSELF ON REBOOT / POWERLOSS
### We'll create a systemd service to make sure the storage is presented whenever the Raspberry Pi Zero reboots:
1. Create a systemd service:
```bash
sudo nano /etc/systemd/system/usb-gadget.service
```
2. Paste this code into the usb-gadget.service file:
```bash
[Unit]
Description=USB Gadget Mass Storage
After=multi-user.target
Requires=local-fs.target

[Service]
Type=oneshot
ExecStart=/sbin/modprobe g_mass_storage file=/piusb.bin stall=0 removable=1
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```
3. Enable the service
```bash
sudo systemctl enable usb-gadget.service
```
4. Reboot the raspberry pi and see if the volumes are available and the rpi zero is acting essentially like a thumb drive when plugged in now.

## AT THIS POINT YOU'VE SUCCESSFULLY SETUP A PI ZERO AS A THUMB DRIVE

# ADD-ON 1 Syncing
# ADD-ON 2 E-Paper Visualization

1 - Enable SPI
- Open the raspberry pi terminal and enter the following command
```bash
sudo raspi-config
```
Choose 3 Interface Options -> I4 SPI -> Yes Enable SPI interface

Now Reboot the Rpi Zero.

2 - Install prerequisites
    - LG Library
```bash
#Open the Raspberry Pi terminal and run the following commands: 
wget https://github.com/joan2937/lg/archive/master.zip
unzip master.zip
cd lg-master
make
sudo make install
#For more details, you can refer to the source code: https://github.com/gpiozero/lg
```
  - BCM2835
```bash
#Open the Raspberry Pi terminal and run the following command
cd ~
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.71.tar.gz
tar zxvf bcm2835-1.71.tar.gz
cd bcm2835-1.71/
sudo ./configure && sudo make && sudo make check && sudo make install
# For more information, please refer to the official website: http://www.airspayce.com/mikem/bcm2835/
```
 - JetsonNano Demo
``` bash
wget https://files.waveshare.com/upload/7/71/E-Paper_code.zip
unzip E-Paper_code.zip -d e-Paper
cd e-Paper/RaspberryPi_JetsonNano/
# Now at e-Paper/RaspberryPi_JetsonNano
cd c
sudo make clean
sudo make -j4 EPD=epd2in13V4
```
 - Function Libraries
```bash
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo pip3 install spidev
```
# Download the refresh script
ADD CODE HERE LATER

Create a service to update the e-paper periodically
```bash
sudo nano /etc/systemd/system/epaper.service
```
Add the content to this file:
```bash
[Unit]
Description=Run screenupdate.py script
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/screenupdate.py
WorkingDirectory=/home/pi
User=pi
```
Create a systemd timer file to run the script so e-paper updates every 30 seconds.
```bash
sudo nano /etc/systemd/system/epaper.timer
```
Add these lines to the file:
```bash
[Unit]
Description=Run screenupdate.py every 30 seconds

[Timer]
OnBootSec=30
OnUnitActiveSec=30
Unit=epaper.service

[Install]
WantedBy=timers.target
```
Enable the timer
```bash
sudo systemctl enable epaper.timer
```
Reboot and your e-paper screen will now start updating every 30 seconds.
