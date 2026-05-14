from src.utils.password_utils import verify_password, hash_password
import pytest


def test_hash_password():
    plain_password = '123456'
    hashed_password = hash_password(plain_password)
    print(f'加密后的密码：{hashed_password}')
    assert hashed_password is not None

def test_verify_password():
    plain_password = '123456'
    hashed_password = hash_password(plain_password)