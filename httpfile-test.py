import httpfile.loader
# noinspection PyUnresolvedReferences
import index


def my_ip():
    r = index.myIp()
    print(r.json())


def post_test():
    r = index.postTest(nick="linux_china", host="httpbin.org")
    print(r.json())


def graphql_test():
    r = index.graphqlDemo(nick="linux_china")
    print(r.json())


if __name__ == '__main__':
    graphql_test()