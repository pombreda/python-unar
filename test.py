#!/usr/bin/python

import sys

from UnAr import Archive, File

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No file specified.")
        sys.exit()

    cmd = " ".join(sys.argv[1:])

    ar = Archive(cmd)
    for f in ar.contents:
        if isinstance(f, File) and f.name.endswith(".txt"):
            with f as p:
                with open(p, "r") as myfile:
                    print(myfile.read())
