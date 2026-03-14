# SR588 Linux Direct USB Printer (No CUPS)

A lightweight Linux printing tool for **SR588 / POS58 USB receipt printers** that avoids CUPS entirely and communicates directly with the printer using **ESC/POS over USB**.

Many inexpensive ESC/POS printers behave unreliably with CUPS because their firmware does not properly clear USB endpoints after printing. This project solves that by **resetting the USB device automatically before each print job** and sending raw ESC/POS data directly to the printer.

The result is a **stable, fast, POS-style printing workflow**.

---

# Features

* Direct USB printing (no CUPS required)
* Automatic USB reset before each job
* Works with **SR588 / POS58 style printers**
* Simple **pipe-based printing workflow**
* Supports **auto-centering**
* Handles **changing USB device numbers**
* Lightweight (single Python script)

---

# Supported Printers

Tested with printers using:

Vendor ID

```
0483
```

Product ID

```
5720
```

Typical models:

* SR588
* POS58
* Generic 58mm ESC/POS printers

---

# Requirements

Linux (tested on Fedora)

Dependencies:

```
python3
pyusb
libusb
gcc
```

Install dependencies:

```
sudo dnf install python3 python3-pip libusb1 libusb1-devel gcc
pip install pyusb
```

---

# Install USB Reset Tool

Many SR588 printers require a USB reset before printing.

Create the reset tool:

```
nano usbreset.c
```

Paste:

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/usbdevice_fs.h>

int main(int argc, char **argv) {
    int fd = open(argv[1], O_WRONLY);
    ioctl(fd, USBDEVFS_RESET, 0);
    close(fd);
}
```

Compile:

```
gcc usbreset.c -o usbreset
sudo mv usbreset /usr/local/bin/
```

---

# Install Printer Script

Save the script as:

```
/usr/local/bin/sr588-print
```

Make executable:

```
sudo chmod +x /usr/local/bin/sr588-print
```

---

# Usage

You can print by piping text into the command:

```
cat receipt.txt | sr588-print
```

or

```
echo "Hello World" | sr588-print
```

---

# Example Receipt

```
^MY STORE
------------------------------
Item A           10.00
Item B           20.00
------------------------------
TOTAL            30.00

^THANK YOU
```

Lines starting with `^` are **automatically centered**.

Output width is formatted for **58mm paper (~32 characters)**.

---

# How It Works

Workflow:

```
text input
   ↓
formatter
   ↓
USB reset
   ↓
ESC/POS data
   ↓
SR588 printer
```

This bypasses CUPS completely and talks directly to the printer.

---

# Why Not CUPS?

Cheap ESC/POS printers often:

* stall USB bulk endpoints
* fail after the first print
* require power cycling

By resetting the device before each job and printing directly via USB, this project avoids those issues.

---

# Limitations

* Designed for **58mm receipt printers**
* Text only (images not implemented yet)
* Assumes **32 character line width**
