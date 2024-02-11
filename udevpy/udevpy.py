#!/usr/bin/python3

import sys
import json


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: <action> <key1=value1> <key2=value2> ...")
        sys.exit(1)

    subsystem = sys.argv[1]
    authorized = sys.argv[2]
    options = {arg.split('=')[0]: arg.split('=')[1] for arg in sys.argv[3:]}
    print(options)