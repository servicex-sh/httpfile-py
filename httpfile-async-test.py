import httpfile.loader
# noinspection PyUnresolvedReferences
import index
import asyncio
from httpx import Response


async def my_ip():
    r: Response = await index.async_my_ip()
    print(r.json())


if __name__ == '__main__':
    asyncio.run(my_ip())
