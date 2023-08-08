import pytest
import sys
import os
import time

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from src.generateEncodingKey import GenerateKey  # noqa: E402


def test__init__():
    gk = GenerateKey(36, 'hex')
    assert gk.key_length == 36
    assert gk.format == 'hex'
    assert abs(gk._GenerateKey__seed - int(time.time())) <= 2
    assert all(True if char in '0123456789abcdef' else False for char in gk._GenerateKey__key)


def test__generate_key():
    gk = GenerateKey(36, 'hex')
    assert all(True if char in '0123456789abcdef' else False for char in next(gk))
    gk = GenerateKey(36, 'int')
    assert all(True if char in '0123456789' else False for char in next(gk))
    gk = GenerateKey(36, 'char')
    assert all(True if char in 'abcdefghijklmnopqrstuvwxyz' else False for char in next(gk))


def test__next__():
    gk = GenerateKey(15, 'hex')
    generated = []
    for _ in range(10):
        key = next(gk)
        assert all(True if char in '0123456789abcdef' else False for char in key)
        assert len(key) == 15
        assert key not in generated
        generated.append(key)


