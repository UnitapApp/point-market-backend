import datetime
import json
from pprint import pprint

import requests


class Zellular:
    queue = []

    @staticmethod
    def push(method, data):
        with open('zellular_queue', 'a') as file:
            file.writelines('\n' + json.dumps({
                'method': method,
                'data': data
            }))

    @staticmethod
    def pull():
        queue = []
        with open('zellular_queue') as file:
            for tx in file.read().split('\n'):
                if tx:
                    queue.append(json.loads(tx))

        with open('zellular_queue', 'w') as file:
            file.write('')

        return queue


    node_url = 'http://5.161.230.186:6001'
    app_name = 'point_market'


    @staticmethod
    def real_push(method, data):
        data = {
            "app_name": 'point_market',
            "transactions": [
                json.dumps({
                    'method': method,
                    'data': data
                })
            ],
            "timestamp": datetime.datetime.now().timestamp(),
        }
        pprint(data)
        print()
        response: requests.Response = requests.put(
            f"{Zellular.node_url}/node/transactions",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"}
        )

        print(response.status_code)
        print(response.text)

    @staticmethod
    def real_pull():
        # response: requests.Response = requests.get(
        #     f"{Zellular.node_url}/node/{Zellular.app_name}/transactions/finalized/last"
        # )
        #
        # print(response.status_code)
        # pprint(response.json()['data']['index'])

        response: requests.Response = requests.get(
            f"{Zellular.node_url}/node/transactions",
            params={
                'app_name': Zellular.app_name,
                'after': 2,
                'states': 'finalized'
            }
        )

        # print(response.status_code)
        pprint(response.json())


if __name__ == '__main__':
    # Zellular.push('hi', {1: 1})
    # Zellular.push('hii', {2: 3})
    # Zellular.pull()

    # Zellular.real_push('create_point', {'name': 'UPX1'})
    # Zellular.real_push('create_point', {'name': 'UPX2'})
    # Zellular.real_push('create_point', {'name': 'UPX3'})
    # Zellular.real_push('create_point', {'name': 'UPX4'})

    Zellular.real_pull()
