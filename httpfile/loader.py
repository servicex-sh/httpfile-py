"""
This module is a custom loader for Python which enables importing http files
directly into Python programs simply through usage of the `import` statement.
You can import this module with `import httpfile.loader` and then afterwards you
can `import your_http_file` which will automatically compile and instantiate
`your_http_file.http` and hook it up into Python's module system.
"""

import sys
import os.path

from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location
import httpx


class SafeDict(dict):
    def __missing__(self, key):
        return ''


# Mostly copied from
# https://stackoverflow.com/questions/43571737/how-to-implement-an-import-hook-that-can-modify-the-source-code-on-the-fly-using

class _HttpfileMetaFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):  # type: ignore
        if path is None or path == "":
            path = [os.getcwd()]  # top level import --
            path.extend(sys.path)
        if "." in fullname:
            *parents, name = fullname.split(".")
        else:
            name = fullname
        for entry in path:
            py = os.path.join(str(entry), name + ".py")
            if os.path.exists(py):
                continue
            httpfile_name = os.path.join(str(entry), name + ".http")
            if os.path.exists(httpfile_name):
                return spec_from_file_location(fullname, httpfile_name, loader=_HttpfileLoader(httpfile_name))

        return None


def create_request(method, url, headers, body):
    def http_request(**params):
        print("=====params======")
        print(params)
        print("=====headers======")
        print(headers)
        print("=====body======")
        print(body)
        print("==============")
        if method == "GET":
            return httpx.get(url, headers=headers)
        elif method == "POST":
            return httpx.post("")
        else:
            pass

    return http_request


class _HttpfileLoader(Loader):
    def __init__(self, filename: str):
        self.filename = filename

    def create_module(self, spec):  # type: ignore
        return None  # use default module creation semantics

    def exec_module(self, module):  # type: ignore
        module.__dict__["myIp"] = create_request('GET', 'https://httpbin.org/ip',
                                                 {"Content-Type": "application/json"},
                                                 '{"id":1, "name":"linux_china"}')


sys.meta_path.insert(0, _HttpfileMetaFinder())
