#!/usr/bin/python

import re
import subprocess
import sys
import binascii
from threading import Timer

TIMEOUT = 5




def _exec_gatttool(mac, timeout, params):

    call = ["gatttool", "-b", mac] + params
    p = subprocess.Popen(call,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    if timeout != -1:
        timer = Timer(timeout, p.kill)

        try:
            timer.start()
            out, err = p.communicate()
        finally:
            timer.cancel()
    else:
        out, err = p.communicate()

    return out.decode("utf-8").split("\n")




def read_measurements(mac, timeout):

    params = ["--char-write-req", "--handle=0x0010", "--value=0100", "--listen"]
    output = _exec_gatttool(mac, timeout, params)
    value = None
    for line in output:
        matches = re.findall("Notification handle = 0x000e value: ([0-9a-f ]+)", line)
        if len(matches) > 0:
            value = matches[0]

    if value is not None:
         return binascii.unhexlify(''.join(value.split()))
    else:
        return ""




def read_battery(mac, timeout):

    params = ["--char-read",  "--handle=0x0018"]
    output = _exec_gatttool(mac, timeout, params)
    for line in output:
        matches = re.findall("Characteristic value/descriptor: ([0-9]+)", line)
        if len(matches) > 0:
            batt = int(matches[0]) * (100.0 / 64.0)
            return "B=%4.1f" % batt

    return ""




def check_args(argv):

    if len(argv) < 2 or len(argv) > 3   :
        print("\nXiaomi bluetooth thermometer / hygrometer")
        print("\nUSAGE: xiaomi <mac> [<timeout>]\n")
        return None, None

    timeout = TIMEOUT if len(argv) == 2 else int(argv[2])

    return sys.argv[1], timeout




if __name__ == "__main__":

    mac, timeout = check_args(sys.argv)

    if ( mac == None):
        exit(1)

    out = read_measurements(mac, timeout)
    out = out + " " + read_battery(mac, -1)
    print(out)

    exit(0)
