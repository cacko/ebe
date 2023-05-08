import csv
from pathlib import Path


def get_columns(csv_path: Path) -> list[str]:
    res = []
    with csv_path.open() as fp:
        cvs_reader = csv.reader(fp)
        for row in cvs_reader:
            res = row
            break
    return res
