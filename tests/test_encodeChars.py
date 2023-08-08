import pytest
import sys
import os
import json

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from src.encodeChars import EncodeDecodeChars  # noqa: E402

char_enc_dec = EncodeDecodeChars()
characters: dict = json.load(open("resources/charPolish.json", "r", encoding="utf-8"))


def test__init__():
    assert char_enc_dec.code_to_char == characters.get("chars")
    assert char_enc_dec.char_to_code == {v: k for k, v in characters.get("chars").items()}
    assert char_enc_dec.name == characters.get("charset")


def test__repr__():
    assert char_enc_dec.__repr__() == f'Character encoding {characters.get("charset")}'


def test__len__():
    assert char_enc_dec.__len__() == len(characters.get("chars"))


def test__BIT_USED():
    assert 2**char_enc_dec.BITS_USED >= len(characters.get("chars"))
    assert 2**(char_enc_dec.BITS_USED - 1) < len(characters.get("chars"))


def test_char_to_bits():
    assert char_enc_dec.char_to_bits(" ") == "0000000"
    assert char_enc_dec.char_to_bits("a") == "1000011"
    assert char_enc_dec.char_to_bits("ą") == "1000100"
    assert char_enc_dec.char_to_bits("9") == "1101111"
    assert char_enc_dec.char_to_bits("\n") == "1110000"
    with pytest.raises(ValueError):
        char_enc_dec.char_to_bits("as")
    with pytest.raises(ValueError):
        char_enc_dec.char_to_bits("😊")
    with pytest.raises(ValueError):
        char_enc_dec.char_to_bits("�")


def test_string_to_bits():
    assert char_enc_dec.string_to_bits(" ") == ["0000000"]
    assert char_enc_dec.string_to_bits("a") == ["1000011"]
    assert char_enc_dec.string_to_bits("ą") == ["1000100"]
    assert char_enc_dec.string_to_bits("9") == ["1101111"]
    assert char_enc_dec.string_to_bits("hEll0 WoR18!") == [
        '1001101', '0100110', '1010001',
        '1010001', '1100110', '0000000',
        '0111101', '1010110', '0110111',
        '1100111', '1101110', '0000001']
    assert char_enc_dec.string_to_bits("aą9 ") ==\
        ["1000011", "1000100", "1101111", "0000000"]
    assert char_enc_dec.string_to_bits("aą9 ą\n") ==\
        ["1000011", "1000100", "1101111", "0000000", "1000100", "1110000"]
    with pytest.raises(ValueError):
        char_enc_dec.string_to_bits("as😊")
    with pytest.raises(ValueError):
        char_enc_dec.string_to_bits("�")


def test_bits_to_char():
    assert char_enc_dec.bits_to_char("0000000") == " "
    assert char_enc_dec.bits_to_char("1000011") == "a"
    assert char_enc_dec.bits_to_char("1000100") == "ą"
    assert char_enc_dec.bits_to_char("1101111") == "9"
    with pytest.raises(ValueError):
        char_enc_dec.bits_to_char("100001")
    with pytest.raises(ValueError):
        char_enc_dec.bits_to_char("100001110")
    with pytest.raises(ValueError):
        char_enc_dec.bits_to_char("1111111") == '1'


def test_bits_to_string():
    assert char_enc_dec.bits_to_string(["0000000"]) == " "
    assert char_enc_dec.bits_to_string(["1000011"]) == "a"
    assert char_enc_dec.bits_to_string(["1000100"]) == "ą"
    assert char_enc_dec.bits_to_string(["1101111"]) == "9"
    assert char_enc_dec.bits_to_string([
        '1001101', '0100110', '1010001',
        '1010001', '1100110', '0000000',
        '0111101', '1010110', '0110111',
        '1100111', '1101110', '0000001']) == "hEll0 WoR18!"
    assert char_enc_dec.bits_to_string(["1000011", "1000100", "1101111", "0000000"]) == "aą9 "
    assert char_enc_dec.bits_to_string(["1000011", "1000100", "1101111", "0000000", "1000100"]) == "aą9 ą"
    with pytest.raises(ValueError):
        char_enc_dec.bits_to_string(["100001"])
    with pytest.raises(ValueError):
        char_enc_dec.bits_to_string(["100001110"])
    with pytest.raises(ValueError):
        char_enc_dec.bits_to_string(["1111111"])