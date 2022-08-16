from pathlib import Path
from pprint import pprint

from httpfile import parse_httpfile


def test_paser():
    http_file = Path(__file__).resolve().parent.parent / "index.http"
    with open(http_file) as f:
        httpfile_text = f.read()
    targets = parse_httpfile(httpfile_text)
    for target in targets:
        pprint(target.__dict__)
        print("==========================")
