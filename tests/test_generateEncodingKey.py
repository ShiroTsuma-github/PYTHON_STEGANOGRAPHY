import pytest
import sys
import os

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from src.encodeChars import EncodeDecodeChars  # noqa: E402



def test__init__():
    assert char_enc_dec.code_to_char == characters.get("chars")
    assert char_enc_dec.char_to_code == {v: k for k, v in characters.get("chars").items()}
    assert char_enc_dec.name == characters.get("charset")
