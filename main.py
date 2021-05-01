#!/usr/bin/env python3

# -------------------------------------------------------------------------
#
# Demonstrates how to send Cisco set of commands from a configuration file.
#
# (C) 2021 Osama Abbas, Cairo, Egypt
# Released under MIT License
#
# Filename: main.py
# Version: Python 3.9.4
# Authors: Osama Abbas (oabbas2512@gmail.com)
# Description:   This program is designed to send Cisco set of commands
#                from a configuration file.
#
# -------------------------------------------------------------------------

import ipaddress
import time
from datetime import datetime, timedelta

import ping3
from colorama import init
from netmiko import Netmiko
from termcolor import cprint

from check_file_status import check_file_status
from clear_file_contents import clear_file_contents
from read_file import read_file

init(autoreset=True)

ping3.EXCEPTIONS = True

# Input file
device_ip_list = read_file("data", "device_ip_list.txt")

# Configuration file
cfg_file = read_file("data", "config.txt")

# Filtration files
success_file = read_file("data", "success.txt")
failure_file = read_file("data", "failure.txt")

delay = 2


def main():

    # Start time
    start_time = datetime.now().replace(microsecond=0)

    # Clear filtration files
    clear_file_contents(success_file)
    clear_file_contents(failure_file)

    # Create a list from device_ip_list
    with open(file=device_ip_list, mode="r") as f:
        ip_list = list(line.strip() for line in f.readlines())

    if not len(ip_list):
        raise SystemExit(
            cprint(
                f"device_ip_list.txt is empty! Please add at least one IP address",
                "yellow",
            )
        )

    # Ping all IP addresses to check reachability
    for ip_addr in ip_list:
        try:
            ipaddress.ip_address(ip_addr).version == 4
            cprint(f"{ip_addr} is a valid IPv4 address", "green")
            try:
                cprint(f"Attempting to ping {ip_addr}...", "magenta")
                ping3.ping(ip_addr)
                cprint(f"Pinging '{ip_addr}' is successful.\n", "green")
                with open(file=success_file, mode="a", encoding="UTF-8") as success:
                    success.write(f"{ip_addr}\n")
            except KeyboardInterrupt:
                cprint("Process interrupted by the user", "yellow")
            except Exception as ex:
                cprint(f"Failed to ping '{ip_addr}'. Error: {ex}\n", "red")
                with open(file=failure_file, mode="a", encoding="UTF-8") as failure:
                    failure.write(f"Failed to ping {ip_addr}: {ex}\n")
        except Exception as err:
            cprint(f"'{ip_addr}' is an invalid IPv4 address\n", "red")

    if check_file_status(failure_file) != 0:
        cprint(
            "Please check 'data/failure.txt' to know which IP addresses that are unreacable\n",
            "yellow",
        )
    else:
        cprint("Congratulations! All IP addresses are reachable\n", "green")

    # Pause for 2 seconds
    time.sleep(delay)

    # Connect to IP addresses in success.txt file
    with open(file=success_file, mode="r") as success_ip_list:
        for ip_addr in success_ip_list:
            ip = ip_addr.rstrip()

            cprint(f"Initiating connection to {ip}...", "magenta")

            cisco_device = {
                "device_type": "cisco_ios_telnet",
                "ip": ip,
                "username": "cisco",
                "password": "cisco",
                "verbose": True,
            }

            try:
                with Netmiko(**cisco_device) as net_connect:
                    cprint(f"Connected to {ip}", "green")
                    net_connect.send_config_from_file(cfg_file)
                    net_connect.save_config()

                cprint(
                    f"Configuration in '{cfg_file}' was sent and saved successfully to '{ip}'",
                    "green",
                )
                cprint(f"'{ip}' session disconnected successfully\n", "green")
            except KeyboardInterrupt:
                cprint("Process interrupted by the user", "yellow")
            except Exception as err:
                cprint(f"Failed to connect to '{ip}': Error: {err}\n", "red")

    elapsed_time = (
        datetime.now().replace(microsecond=0) - start_time - timedelta(seconds=delay)
    )
    cprint(f"Elapsed time: {elapsed_time}", "blue")


if __name__ == "__main__":
    main()
