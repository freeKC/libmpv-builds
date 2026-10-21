#!/usr/bin/env python3
"""Downloads the files listed in recipe-files.lock into a folder, each checked by its SHA-256.

  fetch_recipe_files.py LOCK FOLDER

Each line of the lock: file name, URL, SHA-256. Exit 1 when a download fails or a file does not match its hash.
"""
import hashlib
import pathlib
import sys
import time
import urllib.request


def download(url: str) -> bytes:
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as response:
                return response.read()
        except OSError as error:
            if attempt == 3:
                raise
            print(f'{url}: {error}, again in {5 * (attempt + 1)} s', file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    raise AssertionError


def main(lock: str, folder: str) -> int:
    out = pathlib.Path(folder)
    out.mkdir(parents=True, exist_ok=True)
    failed = False
    for line in pathlib.Path(lock).read_text().splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        name, url, sha256 = line.split()
        if '/' in name or name.startswith('.'):
            print(f'{name}: not a plain file name')
            return 1
        data = download(url)
        digest = hashlib.sha256(data).hexdigest()
        if digest != sha256:
            print(f'{name}: SHA-256 {digest}, expected {sha256}')
            failed = True
            continue
        (out / name).write_bytes(data)
        print(f'{name}: {sha256} ({url})')
    return 1 if failed else 0


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
