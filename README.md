Python httpfile import loader
===============================

# How to use?

* Create http file, such as `httpbin.http`

```
### print my ip
//@name myIp
GET https://httpbin.org/ip
```

* Introduce `httpfile` package
* Write your code:

```python
import httpfile.loader
# noinspection PyUnresolvedReferences
import demo

if __name__ == '__main__':
    r = demo.myIp()
    print(r.json())
```

# Python HTTP Clients

* urllib3: https://urllib3.readthedocs.io/
* Requests: https://requests.readthedocs.io/
* aiohttp: https://docs.aiohttp.org/
* GRequests: https://github.com/spyoungtech/grequests
* HTTPX: https://www.python-httpx.org/