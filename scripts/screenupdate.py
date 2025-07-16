#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import socket
import shutil
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V4
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from datetime import datetime
# Get current date/time
now = datetime.now()
formatted_time = now.strftime("%a %b %d %I:%M %p")  # Format like "Mon Oct 23 02:35 PM"

# Get system uptime
try:
    with open("/proc/uptime", "r") as f:
        uptime = float(f.read().split()[0])
    days, rem = divmod(int(uptime), 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    uptime_text = f"Uptime: {days}d {hours}h {minutes}m"
except:
    uptime_text = "Uptime: N/A"

# Check if the folder /mnt/TeslaCam/TeslaCam exists
tesla_cam_path = "/mnt/TeslaCam/TeslaCam"
drive_status = "Drives Unmounted" if os.path.exists(tesla_cam_path) else "Drives Mounted"

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in13_V4 Demo")

    epd = epd2in13_V4.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)

    # Drawing on the image
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

    hostname = socket.gethostname()  # <-- Get the device hostname
    testIP = "8.8.8.8"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((testIP, 0))
    ip_address = s.getsockname()[0]

    # --- Get used and total disk space ---
    total, used, free = shutil.disk_usage("/")
    total_gb = total // (1024 ** 3)
    used_gb = used // (1024 ** 3)


    # --- Get CPU temperature ---
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_raw = f.read().strip()
            cpu_temp = round(int(temp_raw) / 1000.0, 1)
    except:
        cpu_temp = "N/A"

    # Get disk usage for /mnt/TeslaCam and /mnt/TeslaMusic
    if os.path.exists(tesla_cam_path):
        try:
            cam_usage = shutil.disk_usage("/mnt/TeslaCam").used / (1024 ** 3)  # Convert to GB
            music_usage = shutil.disk_usage("/mnt/TeslaMusic").used / (1024 ** 3)  # Convert to GB
            folder_usage_text = f"Cam: {cam_usage:.1f} GB Music: {music_usage:.1f} GB"
        except:
            folder_usage_text = "Cam: ?? Music: ??"
    else:
        folder_usage_text = "Cam: ?? Music: ??"

    # # partial update
    logging.info("4.show time...")
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)


    # Draw static hostname once
    time_draw.text((10, 5), "Host: " + hostname + " IP: " + ip_address, font=font15, fill=0)
    time_draw.text((10, 20), drive_status, font=font15, fill=0)
    time_draw.text((10, 35), f"Temp: {cpu_temp} C", font=font15, fill=0)
    time_draw.text((10, 50), folder_usage_text, font=font15, fill=0)  # Display folder usage
    time_draw.text((10, 65), uptime_text, font=font15, fill=0)
    time_draw.text((10, 80), f"Time: {formatted_time}", font=font15, fill=0)

    epd.displayPartBaseImage(epd.getbuffer(time_image))
    
    logging.info("Clear...")
    epd.init()


    logging.info("Goto Sleep...")
    epd.sleep()


except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
