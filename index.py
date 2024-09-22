import random

import requests

from utils import set_timeout


def bus_response_handler(res):
    response_data = res.get('responseData', {})
    if type(response_data) is str:  #  等待发车
        return response_data

    car_list = response_data['cars']['car']
    data = []
    for car in car_list:
        data.append((car['stopdis'], car['distance']))

    return data


QUERY_POOL = [
    {
        'url': 'https://gateway.daozhao.com/shanghai/traffic/carMonitor',
        'params': {
            "lineNo": "836",
            "stopId": "7",
            "direction": "1"
        },
        'response_handler': bus_response_handler
    },
    {
        'url': 'https://gateway.daozhao.com/shanghai/traffic/carMonitor',
        'params': {
            "lineNo": "836",
            "stopId": "10",
            "direction": "0"
        },
        'response_handler': bus_response_handler
    }
]


def query(index=0):
    def query_interval():
        nonlocal index
        list_index = index % len(QUERY_POOL)
        print('query_interval times %d, %d of %d' % (index, list_index, len(QUERY_POOL)))

        random_data = random.randint(25, 55)
        print('query after %d seconds' % random_data)

        query_info = QUERY_POOL[list_index]
        res = requests.post(query_info['url'], json=query_info['params']).json()
        data = query_info['response_handler'](res)
        print('data', data)
        set_timeout(query_interval, random_data)
        index += 1

    return query_interval


def start_fn():
    query_interval = query()
    query_interval()


start_fn()
