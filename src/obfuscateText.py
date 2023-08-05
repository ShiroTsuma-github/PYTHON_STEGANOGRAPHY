from encodeChars import EncodeDecodeChars
from generateEncodingKey import GenerateKey


class TextObfuscator():
    def __init__(self,
                 key_length: int = 36,
                 key_format: str = 'hex',
                 char_dict_path: str = 'charPolish.json'):
        self.__key_generator = GenerateKey(key_length, key_format)
        self.__char_encoder = EncodeDecodeChars(char_dict_path)
        self.__key = next(self.__key_generator)

    def __xor(self, a: str, b: str) -> str:
        result =''
        for charA, charB in zip(a, b):
            if charA == charB:
                result += '0'
            else:
                result += '1'
        return result

    def obfuscate(self, text):
        bin_message = self.__char_encoder.string_to_bits(text)
        coded_message = ''
        segment_pointer = 0
        message_pointer = 0
        offset = 0
        self.__key: str = next(self.__key_generator)
        key_binary: List[str] = self.__char_encoder.string_to_bits(self.__key)
        key_nums: list[int] = [int(char, 16) for char in self.__key]
        while True:
            coded_char: str = self.__xor(bin_message[message_pointer], reversed(key_binary[segment_pointer]))
            coded_message += coded_char
            if key_nums[segment_pointer] % 2 == 0:
                offset = 1
            else:
                offset = 2
            if segment_pointer + offset >= len(key_nums):
                segment_pointer = 0
            message_pointer += 1
            segment_pointer += 1
            if segment_pointer >= len(key_nums):
                segment_pointer = 0
            if message_pointer >= len(text):
                break
        return (coded_message, self.__key)

    def deobfuscate(self, coded_message, key):
        bin_message = [coded_message[i:i+self.__char_encoder.BITS_USED]\
                       for i in range(0, len(coded_message), self.__char_encoder.BITS_USED)]
        decoded_message = ''
        segment_pointer = 0
        message_pointer = 0
        offset = 0
        key_binary: List[str] = self.__char_encoder.string_to_bits(key)
        key_nums: list[int] = [int(char, 16) for char in key]
        while True:
            decoded_char: str = self.__xor(bin_message[message_pointer], reversed(key_binary[segment_pointer]))
            decoded_message += self.__char_encoder.bits_to_char(decoded_char)
            if key_nums[segment_pointer] % 2 == 0:
                offset = 1
            else:
                offset = 2
            if segment_pointer + offset >= len(key_nums):
                segment_pointer = 0
            message_pointer += 1
            segment_pointer += 1
            if segment_pointer >= len(key_nums):
                segment_pointer = 0
            if message_pointer >= len(bin_message):
                break
        return decoded_message

    def coded_message_to_string(self, coded_message):
        bin_message = [coded_message[i:i+self.__char_encoder.BITS_USED]\
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
    # print(to.obfuscate('test'))
    # for i in range(10):
    #     print(to.obfuscate('Co tam u ciebie Adamie? Bo u mnie świetnie'))
    mess, key = to.obfuscate('Co tam u ciebie \n\nAdamie? Bo u mnie świetnie')
    print(mess, key)
    print(to.coded_message_to_string(mess))
    print(to.deobfuscate(mess, key))

# '0110101 0100001 0110011 0110101'