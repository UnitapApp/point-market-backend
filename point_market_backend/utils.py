from eth_account import Account
from eth_account.messages import encode_defunct
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
import json
from web3 import Web3


# for tests
def sign(message, private_key=None):
    if private_key is None:
        private_key = Account.create().key

    account = Account.from_key(private_key)
    signature = Account.sign_message(encode_defunct(text=message), private_key).signature.hex()
    return account.address, signature


def get_or_create_user(address):
    return User.objects.get_or_create(
        username=Web3.to_checksum_address(address)
    )[0]


def verify_signature(data):
    address = data.get('address')
    message = data.get('message')
    signature = data.get('signature')

    if not address or not message or not signature:
        raise ValidationError({"message": "Invalid Request"})

    digest = encode_defunct(text=message)
    signer = Account.recover_message(digest, signature=signature)
    if signer == address:
        user = get_or_create_user(address)
        return user, json.loads(message)
    else:
        raise ValidationError({"message": "Invalid Signature"})
