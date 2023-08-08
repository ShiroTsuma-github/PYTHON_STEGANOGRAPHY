import os
from PIL import Image
import csv
import sys

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from src.obfuscateText import TextObfuscator as txob  # noqa: E402


class SteganoImage():
    def __init__(self):
        self.obfs = txob()
        self.width: int = 0
        self.height: int = 0
        self.mode: str = ''

    def __get_coded_message(self, text, key) -> tuple[str, str]:
        return self.obfs.obfuscate(text=text, key=key)

    def __putting_pixels_value_into_file(self, photo) -> None:
        """Function responsible for putting RGB values of photo into csv file

        Args:
            photo (str): string path to chosen photo
        """
        img = Image.open(photo, 'r')
        self.width = img.width
        self.height = img.height
        self.mode = img.mode

        with open(f'{ROOT_DIR}/resources/temp.csv', "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(list(img.getdata()))

    def __csv_row_generator(self):
        total = 0
        with open(f'{ROOT_DIR}/resources/temp.csv', 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                total +=1
                yield row

    def __get_csv_row(self, generator, target_row):
        total = 0
        for i, row in enumerate(generator, start=1):
            total += 1
            if i == target_row:
                yield row

    def __create_image_from_csv(self, output_image_path):
        pixel_values = []

        with open(f'{ROOT_DIR}/resources/temp.csv', 'r') as csvfile:
            for line in csvfile.readlines():
                values = line.strip().split(',')
                pixel_values.append((int(values[0]), int(values[1]), int(values[2])))

        new_image = Image.new(self.mode, (self.width, self.height))
        new_image.putdata(pixel_values)
        new_image.save(output_image_path)

    def __update_csv_value(self, row_position_table, new_value_table):
        updated_rows = []
        with open(f'{ROOT_DIR}/resources/temp.csv', 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            position = 0
            for i, row in enumerate(csvreader, start=1):
                if i != row_position_table[position]:
                    updated_rows.append(row)
                elif i == row_position_table[position]:
                    updated_rows.append(new_value_table[position])
                    if position < len(row_position_table) - 1:
                        position += 1

        with open(f'{ROOT_DIR}/resources/temp.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(updated_rows)

    def __update_row(self, selected, value):
        selected = list(bin(selected))[2:]
        selected[len(selected) - 1] = value
        selected = str(int(''.join(selected), 2))
        return selected

    def encode(self, key, image, text, output=None):
        cdmess, key = self.__get_coded_message(text=text, key=key)
        gen = self.__csv_row_generator()
        self.__putting_pixels_value_into_file(image)
        cdmess = [cdmess[i:i + 7] for i in range(0, len(cdmess), 7)]
        cdmess = '0'.join(cdmess)
        cdmess += '1'
        length_of_key = len(key)
        key = [int(x, 16) for x in key]
        row_point = sum(key)
        changed_indexes = []
        changed_values = []
        total = row_point
        for i, item in enumerate(cdmess):
            if total >= 210:
                print('', end='')
            coding_value = ((i + 1)**2) % length_of_key
            row_value = next(self.__get_csv_row(gen, row_point))
            selected_value = int(row_value[key[coding_value] % 3])
            row_value[key[coding_value] % 3] = self.__update_row(selected_value, cdmess[i])
            changed_indexes.append(total)
            changed_values.append(row_value)
            row_point = key[coding_value] + 1
            total += row_point
        self.__update_csv_value(changed_indexes, changed_values)
        if output is None:
            name = f"{ROOT_DIR}/images/coded_image.png"
        else:
            name = output
        self.__create_image_from_csv(name)

    def decode(self, key, image):
        self.__putting_pixels_value_into_file(image)
        gen = self.__csv_row_generator()
        length_of_key = len(key)
        bin_value = ''
        key = [int(x, 16) for x in key]
        row_point = sum(key)
        i = 0
        while True:
            coding_value = ((i + 1)**2) % length_of_key
            row_value = next(self.__get_csv_row(gen, row_point))
            selected_value = int(row_value[key[coding_value] % 3])
            if (i + 1) % 8 == 0:
                if selected_value % 2 == 1:
                    break
                i += 1
                row_point = key[coding_value]
                continue
            bin_value += str(selected_value % 2)
            row_point = key[coding_value] + 1
            i += 1
        return bin_value


if __name__ == "__main__":
    to = SteganoImage()
    to.encode(
        key="334815546e588d1801dd1cc72b54958",
        image=f"{ROOT_DIR}/images/png2.png",
        text="R")
    bin_value = to.decode(
        key="334815546e588d1801dd1cc72b54958",
        image=f"{ROOT_DIR}/images/coded_image.png")
    print(bin_value)
    print('\n')
    to.encode(
        key="334815546e588d1801dd1cc72b54958",
        image=f"{ROOT_DIR}/images/png2.png",
        text="Ale to zjebane")
    bin_value = to.decode(
        key="334815546e588d1801dd1cc72b54958",
        image=f"{ROOT_DIR}/images/coded_image.png")
    print(bin_value)
