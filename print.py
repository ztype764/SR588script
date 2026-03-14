#!/usr/bin/env python3

import subprocess
import usb.core
import sys
import time

VENDOR = 0x0483
PRODUCT = 0x5720
ENDPOINT = 0x01


def find_usb_path():
    out = subprocess.check_output("lsusb | grep 0483:5720", shell=True).decode()
    parts = out.split()
    bus = parts[1]
    dev = parts[3].replace(":", "")
    return f"/dev/bus/usb/{bus}/{dev}"


def reset_printer():
    path = find_usb_path()
    subprocess.run(["sudo", "usbreset", path], stdout=subprocess.DEVNULL)


def send_to_printer(text):
    dev = usb.core.find(idVendor=VENDOR, idProduct=PRODUCT)

    if dev is None:
        print("Printer not found")
        sys.exit(1)

    dev.set_configuration()

    data = text.encode("utf-8") + b"\n\n\n\x1dV1"
    dev.write(ENDPOINT, data)


def main():

    if len(sys.argv) != 2:
        print("Usage: print.py file.txt")
        sys.exit(1)

    filename = sys.argv[1]

    with open(filename, "r") as f:
        text = f.read()

    reset_printer()
    time.sleep(1)
    send_to_printer(text)


if __name__ == "__main__":
    main()
