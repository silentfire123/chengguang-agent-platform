from src.utils.jwt_utils import encode_jwt, verify_jwt
import pytest

def test_encode_jwt():
    payload = {'id': 123, 'username': 'silentfire'}
    token = encode_jwt(payload)
    print(token)
    assert token is not None

def test_verify_jwt():
    payload = {'id': 123, 'username': 'silentfire'}
    token = encode_jwt(payload)

    payload = verify_jwt(token)
    print(f'payload: {payload}')
    assert payload is not None
    assert token is not None