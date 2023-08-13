import os
from typing import List
from PIL import Image
import sys

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from src.obfuscateText import TextObfuscator as txob  # noqa: E402
from src.steganographImage import SteganoImage as si  # noqa: E402
from src.generateEncodingKey import GenerateKey as gk  # noqa: E402
from src.encodeChars import EncodeDecodeChars as ec  # noqa: E402

if __name__ == "__main__":
    # generateEncodingKey

    # to get key for encoding and decoding use:
    key = gk()
    print(next(key))

    # encodeChars
    # Initialize the encoder
    encoder = ec()

    # Convert a string to binary
    input_text = "Hello World!"
    encoded_bits: List[str] = encoder.string_to_bits(input_text)
    print("Encoded bits:", encoded_bits)

    # Convert binary back to string
    decoded_text = encoder.bits_to_string(encoded_bits)
    print("Decoded text:", decoded_text)

    # Convert a single character to binary
    char_to_convert = "H"
    char_bits = encoder.char_to_bits(char_to_convert)
    print(f"Binary representation of '{char_to_convert}': {char_bits}")

    # Convert binary back to a character
    decoded_char = encoder.bits_to_char(char_bits)
    print(f"Decoded character from bits '{char_bits}': '{decoded_char}'")

    # Initialize the TextObfuscator
    to = txob()

    # obfuscateText
    # Example 1: Obfuscate and deobfuscate a message
    original_message = "kkkkkkkkkkkkkk"
    coded_message, key = to.obfuscate(original_message)
    print("Original Message:", original_message)
    print("Coded Message:", coded_message)
    decoded_message = to.deobfuscate(coded_message, key)
    print("Decoded Message:", decoded_message)

    # Example 2: Obfuscate and deobfuscate a message with a specified key
    original_message = "Adam co u ciebie?"
    key = "123"
    coded_message, key = to.obfuscate(original_message, key)
    print("\nOriginal Message:", original_message)
    print("Coded Message:", coded_message)
    decoded_message = to.deobfuscate(coded_message, key)
    print("Decoded Message:", decoded_message)

    # Example 3: Using the coded_message_to_string function
    coded_message = (
        "101110011001010001000100101011100110010100101100110010000001011100011000100" + 
        "11001100110011001000000101110011001010110011001101000011001010010110011001000010011001100110" + 
        "01100110010001101000110001001100110011001100100010001100101001001100110100001101000110010100" + 
        "1000000110010001100001")
    decoded_message = to.coded_message_to_string(coded_message)
    print("\nDecoded Message from Coded Message:", decoded_message)

    # stenographImage
    # Example: Encode a message into an image
    stenograph = si()
    key = "334815546e588d1801dd1cc72b54958"
    image_path = f"{ROOT_DIR}/resources/images/random.png"
    text = "Robert Kubica"
    output_image_path = "D:/encoded_files.png"
    stenograph.encode(key=key, image=image_path, text=text, output=output_image_path)
    print("Message encoded successfully.\n")

    # Example: Decode a message from an encoded image
    decoded_bin_value = stenograph.decode(key=key, image=output_image_path)
    decoded_text = to.deobfuscate(decoded_bin_value, key)
    print("Decoded Text:", decoded_text)
