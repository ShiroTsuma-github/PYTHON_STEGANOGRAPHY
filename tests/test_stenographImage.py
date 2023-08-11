import pytest
import sys
import os
import os.path
import time
import csv
from PIL import Image


ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from src.steganographImage import SteganoImage  # noqa: E402
from src.obfuscateText import TextObfuscator  # noqa: E402


def test_putting_pixels_value_into_file():
    si = SteganoImage()
    si._SteganoImage__putting_pixels_value_into_file(f'{ROOT_DIR}/resources/images/random.png')
    img = Image.open(f'{ROOT_DIR}/resources/images/random.png', 'r')
    pixels_using_lib = list(img.getdata())
    pixels_from_file = []
    with open(f'{ROOT_DIR}/resources/temp.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            pixel_row = tuple(int(value) for value in row)
            pixels_from_file.append(pixel_row)

    assert pixels_from_file == pixels_using_lib


def test_create_image_from_csv():
    si = SteganoImage()
    si._SteganoImage__putting_pixels_value_into_file(f'{ROOT_DIR}/resources/images/random.png')
    si._SteganoImage__create_image_from_csv("D:/file.png")
    if_exist = os.path.isfile("D:/file.png")
    assert if_exist == True


def test_encode_and_decode():
    si = SteganoImage()
    to = TextObfuscator()

    message = 'My message to you is love'
    key = "1116534635af"
    si.encode(key, f'{ROOT_DIR}/resources/images/random.png', message, "D:/encoded_files.png")
    bin_value = si.decode(key, "D:/encoded_files.png")
    uncoded_message = to.deobfuscate(bin_value, key)
    assert message == uncoded_message

    message = 'My message to you is love'
    key = "1116534635af"
    si.encode(key, f'{ROOT_DIR}/resources/images/random.png', message, "D:/encoded_files.png")
    bin_value = si.decode(key, "D:/encoded_files.png")
    uncoded_message = to.deobfuscate(bin_value, "14312")
    assert message != uncoded_message
    
