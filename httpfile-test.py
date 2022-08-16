import httpfile.loader
# noinspection PyUnresolvedReferences
import index
from httpx import Response


def my_ip():
    r: Response = index.my_ip()
    print(r.json())


def post_test():
    r: Response = index.post_test(nick="linux_china", host="httpbin.org")
    print(r.json())


def graphql_test():
    r: Response = index.graphql_demo(nick="linux_china")
    print(r.json())


if __name__ == '__main__':
    graphql_test()
