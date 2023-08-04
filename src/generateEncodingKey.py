from key_generator.key_generator import generate
import time


class GenerateKey():
    def __init__(self, key_length=32) -> None:
        self.key_length: int = key_length
        self.__seed: int = int(time.time())
        self.__key: str = self.__generate_key()

    def __generate_key(self) -> str:
        key_schema: str = generate(self.key_length,
                                   '', 1, 1,
                                   type_of_value='int',
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
    while True:
        print(next(gen_key))