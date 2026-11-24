"""Graded entrypoint for news-image-20261124 (stdlib only, no network).

Copies the front-page picture stored beside this script into the output
directory named by MAKEFUN_OUTPUT_DIR (default /output), byte for byte,
then prints the destination path, the byte size and the sha256 digest.

Run:  python3 main.py
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE_NAME = "entry.png"


def main():
    source = os.path.join(HERE, SOURCE_NAME)
    if not os.path.isfile(source):
        print("error: %s not found beside main.py" % source,
              file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    destination = os.path.join(out_dir, SOURCE_NAME)
    shutil.copyfile(source, destination)

    with open(destination, "rb") as handle:
        data = handle.read()
    digest = hashlib.sha256(data).hexdigest()
    print(destination)
    print("%d bytes" % len(data))
    print("sha256=%s" % digest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
