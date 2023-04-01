# portscan.py, jtl5jjn

import socket
import sys
from datetime import datetime


# returns target in the form of IPv4 address, start port, and end port from user input
def process_input():
    t = input("Enter a target to scan: ")
    invalid = True
    while invalid:
        try:
            # if hostname, convert to IP address and return
            # if IP address, returns IP address
            t = socket.gethostbyname(t)
            invalid = False
        except socket.error as e:
            print("Error: Invalid hostname or IP address")
            t = input("Enter a target to scan: ")

    # initialize start and end ports
    s, e = 0, 0
    invalid_range = True
    while invalid_range:
        s = input("Please enter the range of ports you would like to scan on the target\n\tEnter a start port: ")
        e = input("\tEnter an end port: ")

        # if neither start or end ports are not ints, throw error
        while not s.isdigit() or not e.isdigit():
            print("Error: Start and end ports must be integers")
            s = input("\tEnter a start port: ")
            e = input("\tEnter an end port: ")

        # if end port is greater than start port, throw error
        if int(e) > int(s):
            invalid_range = False
        else:
            print("Error: Invalid range of ports")
    s, e = int(s), int(e)

    return t, s, e


def scan(t, s, e):
    print("Scanning started at: " + str(datetime.now()))
    print("Please wait, scanning target " + t + " from port " + str(s) + " to " + str(e) + "...")

    try:
        # scan in range of ports from start to end port exclusive
        for port in range(s, e):
            mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 3 second timeout per port
            mysocket.settimeout(5)

            # if connect_ex returns 0, display that port is open, else display it is closed
            res = mysocket.connect_ex((t, port))
            if res == 0:
                print("Port " + str(port) + ":\tOpen")
            else:
                print("Port " + str(port) + ":\tClosed")

        print("\nPort Scanning Completed!")

    # catch error in case server does not respond
    except socket.error:
        print("Error: Server not responding")
        sys.exit()


if __name__ == "__main__":
    target, start_port, end_port = process_input()
    scan(target, start_port, end_port)
