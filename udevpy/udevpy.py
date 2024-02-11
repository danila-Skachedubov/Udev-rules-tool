import sys
import json


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: <action> <key1=value1> <key2=value2> ...")
        sys.exit(1)