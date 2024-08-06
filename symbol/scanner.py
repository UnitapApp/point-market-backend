import re
from pprint import pprint
from time import sleep

from eth_abi import decode
from eth_utils import keccak
from web3 import Web3


class Scanner:
    def __init__(self, web3: Web3):
        self.web3 = web3

    def get_block(self, block_number):
        return dict(self.web3.eth.get_block(block_number, full_transactions=True))

    @staticmethod
    def get_method_id(function_signature):
        function_signature_hash = keccak(text=function_signature)
        return '0x' + function_signature_hash[:4].hex()

    def get_transactions(self, from_block_number, to_block_number):

        transactions = []
        for block_number in range(from_block_number, to_block_number + 1):
            transactions += self.get_block(block_number)['transactions']

        return transactions


    @staticmethod
    def get_params_types(function_signature):
        params_type = re.findall(r'\((.*?)\)', function_signature)[0].split(',')
        if len(params_type) == 1 and params_type[0] == '':
            params_type = []
        return params_type


    def process_transaction(self, transaction, contract_address, function_signature, params_mask):
        # check contract address
        if transaction['to'].lower() == contract_address.lower():
            # check method
            method_id = self.get_method_id(function_signature)
            if transaction['input'].hex().startswith(method_id):
                # check params
                parameter_types = self.get_params_types(function_signature)
                decoded_params = decode(parameter_types, bytes.fromhex(transaction['input'].hex()[10:]))
                for i in range(len(parameter_types)):
                    param = params_mask[i]
                    if isinstance(param, str):
                        param = param.lower()

                    decoded_param = decoded_params[i]
                    if isinstance(decoded_param, str):
                        decoded_param = decoded_param.lower()

                    if param not in ('*', decoded_param):
                        return False, decoded_params

                return True, decoded_params
        return False, None


def main():
    contract_address = '0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85'
    function_signature = 'transfer(address,uint256)'
    block_number = 123358809

    s = Scanner(RPCs[10])
    transactions = s.get_transactions(block_number - 5, block_number + 5)
    for tx in transactions:
        success, params = s.process_transaction(tx, contract_address, function_signature, ['0x953f33746b65b8628b93b42a28ce2a1fa67a1fb0', '*'])
        if success:
            print(params)


if __name__ == '__main__':
    main()
