from key_generator.key_generator import generate
import time


class GenerateKey():
    """Generate a key for encoding and decoding data.
    The key is a string of numbers.
    The length of the key is set by the key_length parameter.
    The key is generated using the key_generator library.
    To get key you have to use next() method.
    Possible formats of the key: `'int', 'hex', 'char'`
    """
    def __init__(self, key_length=32, format='int') -> None:
        self.key_length: int = key_length
        self.format: str = format
        self.__seed: int = int(time.time())
        self.__key: str = self.__generate_key()

    def __generate_key(self) -> str:
        key_schema: str = generate(self.key_length,
                                   '', 1, 1,
                                   type_of_value=self.format,
                                   seed=self.__seed).get_key()
        return key_schema

    def __next__(self) -> str:
        self.__seed -= 100
        self.__key = self.__generate_key()
        return self.__key

    def __iter__(self):
        raise NotImplementedError


if __name__ == "__main__":
    gen_key = GenerateKey()
    print(next(gen_key))
