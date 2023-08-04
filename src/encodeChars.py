from typing import List
import json
import os

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


class EncodeDecodeChars:
    """Class for encoding and decoding characters to and from binary strings of length 8.
    """
    def __init__(self, char_dict_path='charDict.json'):
        self.__raw_dict: dict = self.__load_json(f"{ROOT_DIR}/resources/{char_dict_path}")
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

    def char_to_bits(self, char: str) -> str:
        """Converts a character to a binary string of length 8,
        based on the character encoding provided in the `charDict.json` file.

        Args:
            char (str): Character to be converted to binary

        Returns:
            str: Returns a binary string of length 8
        """
        result: str = str(bin(int(self.char_to_code.get(char, 127)))).replace("0b", "")
        padding: int = 8 - len(result)
        return "0" * padding + result

    def bits_to_char(self, bits: str) -> str:
        """Converts a binary string of length 8 to a character,

        Args:
            bits (str): Binary string of length 8

        Returns:
            str: Character represented by the binary string
        """
        result: str = self.code_to_char.get(str(int(bits, 2)))
        return result

    def string_to_bits(self, text: str) -> List[str]:
        """Converts a string to a list of binary strings of length 8

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
        """Converts a list of binary strings of length 8 to a string

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
    temp = encoder.string_to_bits("Hello World!")
    print(temp)
    print(encoder.bits_to_string(temp))
