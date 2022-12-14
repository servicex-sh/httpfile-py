Python httpfile import loader
===============================

![import httpfile in Python](./py_import_httpfile.png)

# How to use?

* Create http file, such as `httpbin.http`

```
### print my ip
//@name my-ip
GET https://httpbin.org/ip
```

* Add `httpfile-py` package in `requirements.txt` or other configuration file
* Write your code:

```python
import httpfile.loader
# noinspection PyUnresolvedReferences
import httpbin
from httpx import Response

if __name__ == '__main__':
    r: Response = httpbin.my_ip()
    print(r.json())
```

# Async support

If you want to use async feature, please add `async_` prefix to request name, code as following:

```python
import httpfile.loader
# noinspection PyUnresolvedReferences
import httpbin
import asyncio
from httpx import Response


async def my_ip():
    r: Response = await httpbin.async_my_ip()
    print(r.json())


if __name__ == '__main__':
    asyncio.run(my_ip())

```

**Attention**: don't forget to add `asyncio` package!

# Python HTTP Clients

* urllib3: https://urllib3.readthedocs.io/
* Requests: https://requests.readthedocs.io/
* aiohttp: https://docs.aiohttp.org/
* GRequests: https://github.com/spyoungtech/grequests
* HTTPX: https://www.python-httpx.org/

httpfile-py uses HTTPX as http client.

# References

* https://servicex.sh/