# TesTrove
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
Edit `/boot/firmware/config.txt` if the line doesn’t exist in the [all] section; Add:

```bash
dtoverlay=dwc2
```
*(This ensures USB storage drivers load correctly.)*

### Edit `cmdline.txt`
Append to `/boot/firmware/cmdline.txt` (after `rootwait`):

```bash
modules-load=dwc2,g_ether
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

Run this command to pre-allocate space for your USB drive (adjust `count=16384` as needed for larger SD cards)
Make the bin size something much less than the size of your sd card. For example, for a 128GB card, only use 90GB, for a 256GB card only use 200GB. The command is:

```bash
sudo dd bs=1M if=/dev/zero of=/piusb.bin count=16384 status=progress  # 16GB = 16384 × 1MB
```
*Note: This step may take hours and hours depending on the size of bin you are making.*

---

## MAKE SOME MOUNT POINTS

Create directories for storage partitions:

```bash
sudo mkdir /mnt/usb_share    # System-accessible mount point shared over usb
sudo mkdir /mnt/TeslaCam     # Will act as a mount point for DashCam partition
sudo mkdir /mnt/TeslaMusic   # Will act as a mount point for Music partition
```

---

## EDIT `fstab` FILE

Append to `/etc/fstab` to auto-mount the drive on boot:

```bash
/piusb.bin /mnt/usb_share auto users,umask=000 0 2
```

**Reboot** after editing `fstab`.

---

## USAGE COMMANDS FOR STORAGE DEVICE

### Activate USB Storage
Attach the Pi Zero to a Windows PC. !!BE SURE TO USE THE 2nd microUSB port which supports data AND power.!! We can now activate the storage so it appears as a drive for the windows machine, (just like it will when it is plugged into your tesla later.

## Presenting and Removing the Storage over USB:

To Present the storage:

```bash
sudo modprobe g_mass_storage file=/piusb.bin stall=0 ro=1
```
You should be able to hear the drive appearing on the USB on your windows machine.

To Remove the storage:

```bash
sudo modprobe -r g_mass_storage
```

You can try toggling these commands to make sure it works at this point, but then leave it connected in order to do the next step.

# FORMAT THE DRIVE INTO MULTIPLE PARTITIONS USING WINDOWS.
once you can see the drive in windows when the raspberry pi zero is plugged into it.
You may have to use the computer management window to see the volume. (run compmgmt.msc)
Use **DiskPart** (Windows Command Prompt) :


1. Run Diskpart: `diskpart`
2.  View your volumes `list disk`.
3. Select target disk: `select disk [number]` (replace `[number]` with the volume the rpi is presenting windows).
4. Create the 1st partition (Music Partition:
   - Primary partition: Size = 8GB (for Music).
     ```powershell
     create partition primary size=8192
     ```
   - Format as exfat).
     ```powershell
     list partition  # Confirm partitions
     select partition 1  # Select DashCam partition
     create partition primary
     select partition 2  # Select TeslaMusic partition
     create partition primary
     ```
5. Format partitions as exFAT:
   ```powershell
   format fs=exfat quick  # Use exFAT for cross-platform compatibility
   ```

6. Go back to the Raspberry Pi and install `kpartx` which will let us mount our two partitions separately:
   ```bash
   sudo apt update && sudo apt install kpartx
   sudo kpartx -a /piusb.bin
   ```

### Detach USB Storage
To unmount safely:

```bash
sudo modprobe -r g_mass_storage
```
