import datetime
import json
from pprint import pprint
import requests

from core.models import ZellularTransaction


class ZellularStream:
    queue = []

    # @staticmethod
    # def push(method, data):
    #     with open('zellular_queue', 'a') as file:
    #         file.writelines('\n' + json.dumps({
    #             'method': method,
    #             'data': data
    #         }))
    #
    # @staticmethod
    # def pull():
    #     queue = []
    #     with open('zellular_queue') as file:
    #         for tx in file.read().split('\n'):
    #             if tx:
    #                 queue.append(json.loads(tx))
    #
    #     with open('zellular_queue', 'w') as file:
    #         file.write('')
    #
    #     return queue

    node_url = 'http://5.161.230.186:6001'
    app_name = 'point_market'

    @staticmethod
    def push(method, data):
        ZellularTransaction.objects.create(
            type=ZellularTransaction.PUSH,
            method=method,
            data=data
        )

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

        response: requests.Response = requests.put(
            f"{ZellularStream.node_url}/node/transactions",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"}
        )

        return response

    @staticmethod
    def pull(last_pulled_index):

        response: requests.Response = requests.get(
            f"{ZellularStream.node_url}/node/{ZellularStream.app_name}/transactions/finalized/last"
        )
        if response.status_code == 200:
            data = response.json()['data']
            latest_index = data.get('index', 0)
        else:
            raise Exception(response.text)

        if latest_index > last_pulled_index:
            response: requests.Response = requests.get(
                f"{ZellularStream.node_url}/node/transactions",
                params={
                    'app_name': ZellularStream.app_name,
                    'after': last_pulled_index,
                    'states': 'finalized'
                }
            )
            if response.status_code == 200:
                data = []
                for row in response.json()['data']:
                    row = json.loads(row['body'])
                    data.append(row)
                    ZellularTransaction.objects.create(
                        type=ZellularTransaction.PULL,
                        method=row['method'],
                        data=row['data']
                    )

                return data, latest_index
            else:
                raise Exception(response.text)

        return [], last_pulled_index


if __name__ == '__main__':
    # Zellular.push('hi', {1: 1})
    # Zellular.push('hii', {2: 3})
    # Zellular.pull()

    # Zellular.real_push('create_point', {'name': 'UPX1'})
    # Zellular.real_push('create_point', {'name': 'UPX2'})
    # Zellular.real_push('create_point', {'name': 'UPX3'})
    # Zellular.real_push('create_point', {'name': 'UPX4'})

    pprint(
        # Zellular.real_pull(0)
    )
