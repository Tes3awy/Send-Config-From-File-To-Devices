[![Tested on Python 3.9.4](https://img.shields.io/badge/Tested%20-Python%203.9.4-blue.svg?logo=python)](https://www.python.org/downloads)
[![Contributions Welcome](https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=7206BB)]()
[![License](https://img.shields.io/github/license/Tes3awy/Cisco-Configuration-Using-Python-Jinja-CSV)](https://github.com/Tes3awy/Cisco-Configuration-Using-Python-Jinja-CSV/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Send Cisco Commands to Multiple Network Devices

This program is designed to send a set of Cisco commands to multiple network devices from text files.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Best Case Scenario](#best-case-scenario)
4. [TODO](#todo)

### Installation

```bash
$ git clone https://github.com/Tes3awy/Send-Config-From-File-To-Devices.git
$ cd Send-Config-From-File-To-Devices
$ pip install -r requirements.txt
```

### Usage

In `main.py` file, provide the `username` and `password` for `cisco_device` variable:

```python
cisco_device = {
      "device_type": "cisco_ios_telnet", # or cisco_ios for SSH
      "ip": ip,
      "username": "cisco", # <---
      "password": "cisco", # <---
      "verbose": True,
}
```

```python
python main.py
```

**The Python script runs as following:**

1. Reads IP addresses in `data/device_ip_list.txt`.
2. Checks if those IP addresses are valid IPv4 addresses.
3. Pings those IP addresses to check reachability.
   - If an IP address is <span style="color: red;">UNREACHABLE</span> for whatever reason, then this IP is added to `data/failure.txt` with its error message.
   - If an IP address is <span style="color: green;">REACHABLE</span>, then this IP is added to `data/success.txt`.
4. Reads each IP addresse in `data/success.txt` one by one.
5. Initiates a connection.
6. Sends commands from `data/config.txt` to the device of that IP address.
7. Saves the configuration on the device.
8. Terminates the connection.

### Best Case Scenario

1. You want to add the same exact set of commands to all the devices in your network. Then this script is the best option for this task.
2. Username you are logging in with has `privilege 15` in it. **i.e.**

<pre>
username cisco <strong>privilege 15</strong> algorithm-type scrypt secret cisco
</pre>

> This Python script neither checks enable mode nor config mode. It's left to the user to add `(conf)igure (t)erminal` in the `data/config.txt` file.

### TODO

1. [ ] Enable MultiThreading.
