from pathlib import Path
from pprint import pprint

from httpfile import parse_httpfile, SafeDict
from string import Template


def test_safe_dict():
    params = {'nick': 'linux_china'}
    t = Template("Hello ${nick}, your age ${age}, uuid: ${uuid}")
    text = t.substitute(SafeDict(params))
    print(text)


def test_paser():
    http_file = Path(__file__).resolve().parent.parent / "index.http"
    with open(http_file) as f:
        httpfile_text = f.read()
    targets = parse_httpfile(httpfile_text)
    for target in targets:
        pprint(target.__dict__)
        print("==========================")
