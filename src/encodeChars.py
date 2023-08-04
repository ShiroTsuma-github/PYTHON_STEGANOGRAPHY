from typing import List
import json
import os
from math import log

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


class EncodeDecodeChars:
    """Class for encoding and decoding characters to and from binary strings
    of length based on char*.json.
    """
    def __init__(self, char_dict_path='charPolish.json'):
        self.__raw_dict: dict = self.__load_json(f"{ROOT_DIR}/resources/{char_dict_path}")
        self.BITS_USED: int = self.__get_bits()
        self.code_to_char: dict = self.__raw_dict.get("chars")
        self.char_to_code: dict = {v: k for k, v in self.code_to_char.items()}
        self.name: str = self.__raw_dict.get('charset')

    def __repr__(self) -> str:
        return f"Character encoding {self.name}"

    def __len__(self) -> int:
        return len(self.__raw_dict.get('chars'))

    def __load_json(self, path: str) -> dict:
        with open(path, "r", encoding='utf-8') as json_file:
            return json.load(json_file)

    def __get_bits(self) -> int:
        n: int = len(self.__raw_dict.get('chars'))
        ans: int = int(log(n - 1) / log(2)) + 1
        return ans

    def char_to_bits(self, char: str) -> str:
        """Converts a character to a binary string of length
        based on the number of characters in the dictionary,
        based on the character encoding provided in the `char*.json` file.

        Args:
            char (str): Character to be converted to binary

        Raises:
            ValueError: When more than one character is provided
            or the character is not in the dictionary

        Returns:
            str: Returns a binary string of length `self.BITS_USED`
        """
        if len(char) > 1:
            raise ValueError("Only single characters are allowed")
        result: str = str(bin(int(self.char_to_code.get(char, -1)))).replace("0b", "")
        if result == "-1":
            raise ValueError("Character not in dictionary. Change the dictionary or the character")
        padding: int = self.BITS_USED - len(result)
        return "0" * padding + result

    def bits_to_char(self, bits: str) -> str:
        """Converts a binary string of length based on `self.BITS_USED` to a character,

        Args:
            bits (str): Binary string of length `self.BITS_USED`

        Returns:
            str: Character represented by the binary string
        """
        if len(bits) != self.BITS_USED:
            raise ValueError(f"Binary string must be of length {self.BITS_USED}")
        result: str = self.code_to_char.get(str(int(bits, 2)), -1)
        if result == -1:
            raise ValueError("Bits outside of dictionary. Change the dictionary.")
        return result

    def string_to_bits(self, text: str) -> List[str]:
        """Converts a string to a list of binary strings of length `self.BITS_USED`

        Args:
            text (str): String to be converted to binary

        Returns:
            List[str]: Returns a list of binary encoded characters
        """
        result: List[str] = []
        for char in text:
            result.append(self.char_to_bits(char))
        return result

    def bits_to_string(self, bits: List[str]) -> str:
        """Converts a list of binary strings of length `self.BITS_USED` to a string

        Args:
            bits (List[str]): List of binary characters

        Returns:
            str: Text represented by the binary strings
        """
        result: str = ""
        for bit in bits:
            result += self.bits_to_char(bit)
        return result


if __name__ == "__main__":
    encoder = EncodeDecodeChars()
    print(encoder)
    temp = encoder.string_to_bits("hEll0 WoR18!")
    print(temp)
    print(encoder.bits_to_string(temp))
