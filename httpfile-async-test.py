import httpfile.loader
# noinspection PyUnresolvedReferences
import index
import asyncio


async def my_ip():
    r = await index.async_my_ip()
    print(r.json())


if __name__ == '__main__':
    asyncio.run(my_ip())
