# MIT License
#
# Copyright (c) 2023 Andrew Kushyk
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import nmap
import re


def is_valid_ip(ip_address):
    pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    pattern2 = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$")
    return pattern.match(ip_address) or pattern2.match(ip_address) is not None


def start_scanning(nmp, tar, opt):
    print(f"Scanning {tar} using {opt} ...")
    nmp.scan(tar, arguments=opt)
    print("Scanning finished.")


def show_results(nmp):
    for host in nmp.all_hosts():
        print(f"Host: {host} ({nmp[host].hostname()})")
        print(f"State: {nmp[host].state()}")
        for protocol in nmp[host].all_protocols():
            print(f"Protocol: {protocol}")
            port_info = nmp[host][protocol]
            for port, state in port_info.items():
                print(f"Port: {port}\tState: {state}")


while True:
    target = input("Enter target ip address: ")
    if not is_valid_ip(target):
        print("Invalid IP address!")
    else:
        break

while True:
    nm = nmap.PortScanner()
    mode = int(input("Do you want (1) default scan, (2) custom or (0) exit?: "))
    if mode == 0:
        break
    elif mode == 1:
        options = "-sV -sC scan_results"
        start_scanning(nm, target, options)
        show_results(nm)
        break
    elif mode == 2:
        options = input("Enter your nmap scan options: ") + " scan_results"
        start_scanning(nm, target, options)
        show_results(nm)
        break
    else:
        print("Invalid mode!")
