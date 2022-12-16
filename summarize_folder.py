import csv
import datetime
import hashlib
import os
from datetime import datetime
from io import RawIOBase
from os import path
from typing import Iterable

BUFFER_SIZE = 128 * 2 ** 10  # 128kb


def sha256sum(filename: str | os.PathLike[str]):
    h = hashlib.sha256()
    b = bytearray(BUFFER_SIZE)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        f: RawIOBase
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()


def summarize_file(root: str | os.PathLike[str], full_path: str | os.PathLike[str]):
    """Returns the following things of the specified file as an array:

        - A relative path from the root to this file
        - The SHA256 hash sum of the file
        - The last modified date of this file as ISO string
        - The size of the file in bytes
    """
    hash_sum = sha256sum(full_path)
    date_changed = datetime.fromtimestamp(os.path.getmtime(full_path))
    date_changed_str = date_changed.isoformat(sep=' ', timespec='seconds')
    size = os.path.getsize(full_path)
    rel_path = path.relpath(full_path, root)

    return [rel_path, hash_sum, date_changed_str, size]


def summarize_all_files(folder_path: str | os.PathLike[str]) -> Iterable[Iterable]:
    """Iterate all the files in the given folder (including subfolders) in alphabetical order."""
    for root, dirs, files in os.walk(folder_path):
        # ensure consistent order across platforms etc.
        dirs.sort()
        files.sort()
        for file in files:
            yield summarize_file(folder_path, path.join(root, file))


if __name__ == '__main__':
    cur_dir = os.getcwd()
    output_file = path.join(cur_dir, "summary.csv")
    headers = ['PATH', 'HASHSUM (SHA256)', 'DATE_CHANGED', 'SIZE (bytes)']

    dialect = csv.excel()
    dialect.doublequote = False
    dialect.escapechar = '\\'
    dialect.quoting = csv.QUOTE_NONNUMERIC

    print(f"Summarizing files in '{cur_dir}' ...")
    with open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, dialect)
        csv_writer.writerow(headers)
        csv_writer.writerows(summarize_all_files(cur_dir))

    print(f"Finished summarizing folder into {output_file}")
