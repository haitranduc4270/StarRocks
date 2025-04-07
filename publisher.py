import sys
import random
import time
from kafka import KafkaProducer


def genUid(s=10000):
    return random.randint(1, s)


def getSite():
    site_scope = ['https://www.starrocks.io/'] * 100 + ['https://www.starrocks.io/blog'] * 34 + \
                  ['https://www.starrocks.io/product/community'] * 12 + ['https://docs.starrocks.io/'] * 55
    idx = random.randint(0, len(site_scope) - 1)
    return site_scope[idx]


def getTm():
    delay_jitter = random.randint(-1800, 0)
    chance = random.randint(0, 3)
    return int(time.time() + delay_jitter * chance)



def gen():
    data = """{ "uid": %d, "site": "%s", "vtime": %s } """ % (genUid(), getSite(), getTm())
    return data


def main():
    producer = KafkaProducer(bootstrap_servers='192.168.0.112:9092')

    while True:
        data = gen().encode('UTF-8')
        print(data)
        producer.send('test2', data)
        time.sleep(1)


if __name__ == '__main__':
    main()
