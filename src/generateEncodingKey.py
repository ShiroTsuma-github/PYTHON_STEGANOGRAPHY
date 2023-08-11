from key_generator.key_generator import generate
import time
from random import randint


class GenerateKey():
    """Generate a key for encoding and decoding data.
    The key is a string of numbers.
    The length of the key is set by the key_length parameter.
    The key is generated using the key_generator library.
    To get key you have to use next() method.
    Possible formats of the key: `'int', 'hex', 'char'`
    """

    def __init__(self, key_length=32, format='int') -> None:
        """After creation and passing arguments you invoke next key generation,
        by using `next(Class)`

        Args:
            key_length (int, optional): Lenght of key to generate. Defaults to 32.
            format (str, optional): Format of key. Valid `'int', 'hex', 'char'`.
              Defaults to 'int'.
        """
        self.key_length: int = key_length
        """Length of key"""
        self.format: str = format
        """Format of key"""
        self.__seed: int = int(time.time())
        self.__key: str = self.__generate_key()

    def __generate_key(self) -> str:
        key_schema: str = generate(self.key_length,
                                   '', 1, 1,
                                   type_of_value=self.format,
                                   seed=self.__seed).get_key()
        return key_schema

    def __next__(self) -> str:
        self.__seed -= randint(1, 100)
        self.__key = self.__generate_key()
        return self.__key

    def __iter__(self):
        raise NotImplementedError
