import pytest
import sys
import os
import random
import jellyfish

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from src.obfuscateText import TextObfuscator  # noqa: E402


def test_obfuscate_and_deobfuscate():
    to = TextObfuscator()
    message = 'This is a test message'
    coded_message, key = to.obfuscate(message)
    assert to.deobfuscate(coded_message, key) == message


def test_xor_binary_strings():
    to = TextObfuscator()
    assert to._TextObfuscator__xor('111010101', '101010101') == '010000000'
    assert to._TextObfuscator__xor('000000000', '111111111') == '111111111'
    assert to._TextObfuscator__xor('101010101', '010101010') == '111111111'


def test_coded_message():
    to = TextObfuscator()
    message = 'This is a test message'
    coded_message, key = to.obfuscate(message)
    assert coded_message != message


def test_similiarity():
    to = TextObfuscator()
    key_format_hex: list[str] = ['0', '1', '2', '3', '4', '5', '6', '7',
                                 '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    message = 'This is a test message'
    for __ in range(16):
        for i in range(16):
            key = ''.join(random.choices(key_format_hex, k=3 + i))
            coded_message, _ = to.obfuscate(message, key)
            coded_wrong = to.deobfuscate(coded_message, key[1:])
            assert jellyfish.jaro_similarity(message, coded_message) < 0.8
            assert jellyfish.jaro_similarity(message, coded_wrong) < 0.8
