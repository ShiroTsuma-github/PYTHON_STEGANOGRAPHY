from typing import List
import sys
import os

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from src.encodeChars import EncodeDecodeChars       # noqa: E402
from src.generateEncodingKey import GenerateKey     # noqa: E402


class TextObfuscator():
    """Obfuscate and deobfuscate text using XOR cipher."""
    def __init__(self,
                 key_length: int = 36,
                 key_format: str = 'hex',
                 char_dict_path: str = 'charPolish.json'):
        self.__key_generator = GenerateKey(key_length, key_format)
        self.__char_encoder = EncodeDecodeChars(char_dict_path)
        self.__key = next(self.__key_generator)
        self.char_length = self.__char_encoder.BITS_USED

    def __xor(self, a: str, b: str) -> str:
        """XOR two binary strings of the same length.

        Args:
            a (str): string of 0s and 1s
            b (str): string of 0s and 1s

        Returns:
            str: XORed string of 0s and 1s
        """
        result = ''
        for charA, charB in zip(a, b):
            if charA == charB:
                result += '0'
            else:
                result += '1'
        return result

    def __xor_list(self, char: str, key: list[str]) -> str:
        for charKey in key:
            char = self.__xor(char, charKey)
        return char

    def obfuscate(self, text, key=None) -> tuple[str, str]:
        """Obfuscate text using XOR cipher. The key is generated using the GenerateKey class.
        Text is first converted to binary string.
        Then each character is XORed with a reversed segment of the key.
        The segment is chosen based on the value of the key. If the value is even,
        the key segment pointer increases by 1, else 2.
        If the segment pointer is greater than the length of the key, it is set to 0.
        Segments of key are also cobnverted to binary strings.

        Args:
            text (str): Message to obfuscate.
            key (str, optional): Key to use for obfuscation. Defaults to None.

        Returns:
            tuple[str, str]: Returns a tuple of obfuscated message and the key used.
        """
        bin_message = self.__char_encoder.string_to_bits(text)
        coded_message = ''
        segment_pointer = 0
        message_pointer = 0
        if key is None:
            self.__key: str = next(self.__key_generator)
        else:
            self.__key: str = key
        key_binary: List[str] = list(reversed(self.__char_encoder.string_to_bits(self.__key)))
        while True:
            coded_char: str = self.__xor_list(bin_message[message_pointer], reversed(key_binary[segment_pointer:]))
            coded_message += coded_char
            message_pointer += 1
            if segment_pointer + 1 >= len(key_binary):
                segment_pointer = 0
            else:
                segment_pointer += 1
            if message_pointer >= len(text):
                break
        return (coded_message, self.__key)

    def deobfuscate(self, coded_message, key):
        bin_message = [coded_message[i:i + self.__char_encoder.BITS_USED]
                       for i in range(0, len(coded_message), self.__char_encoder.BITS_USED)]
        decoded_message = ''
        message_pointer = 0
        segment_pointer = 0
        key_binary: List[str] = list(reversed(self.__char_encoder.string_to_bits(key)))
        while True:
            decoded_char: str = self.__xor_list(bin_message[message_pointer], reversed(key_binary[segment_pointer:]))
            try:
                decoded_message += self.__char_encoder.bits_to_char(decoded_char)
            except ValueError:
                decoded_message += ' '
            message_pointer += 1
            if segment_pointer + 1 >= len(key_binary):
                segment_pointer = 0
            else:
                segment_pointer += 1
            if message_pointer >= len(bin_message):
                break
        return decoded_message

    def coded_message_to_string(self, coded_message):
        bin_message = [coded_message[
            i:i + self.__char_encoder.BITS_USED]
            for i in range(0, len(coded_message), self.__char_encoder.BITS_USED)]
        decoded_message = ''
        for char in bin_message:
            try:
                decoded_message += self.__char_encoder.bits_to_char(char)
            except ValueError:
                decoded_message += ' '
        return decoded_message


if __name__ == "__main__":
    to = TextObfuscator()
    mess, key = to.obfuscate('kkkkkkkkkkkkkk')
    print(mess, key)
    print(to.coded_message_to_string(mess))
    print(to.deobfuscate(mess, key))
    mess, key = to.obfuscate('Adam co u ciebie?', '123')
    print(mess, key)
    print(to.coded_message_to_string(mess))
    print(to.deobfuscate(mess, '123'))
