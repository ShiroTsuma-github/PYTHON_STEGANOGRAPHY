import os
from PIL import Image
import csv
import sys

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from src.obfuscateText import TextObfuscator as txob  # noqa: E402


class image_stenographing():
    Width: int = 0
    Height: int = 0
    Mode: str = ''

    def __init__(self):
        self.obfs = txob()

    def __get_coded_message(self, text, key) -> tuple[str, str]:
        return self.obfs.obfuscate(text=text, key=key)

    def __putting_pixels_value_into_file(self, photo, filecsv) -> None:
        """Function responsible for putting RGB values of photo into csv file

        Args:
            photo (str): string path to chosen photo
        """
        img = Image.open(photo, 'r')
        global Width
        Width = img.width
        global Height
        Height = img.height
        global Mode
        Mode = img.mode

        with open(filecsv, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(list(img.getdata()))

    def __csv_row_generator(self, file_path):
        with open(file_path, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                yield row

    def __get_csv_row(self, generator, target_row):
        for i, row in enumerate(generator, start=1):
            if i == target_row:
                return row
    
    def __create_image_from_csv(self, csv_file_path, output_image_path):
        pixel_values = []

        with open(csv_file_path, 'r') as csvfile:
            for line in csvfile.readlines():
                values = line.strip().split(',')
                pixel_values.append((int(values[0]), int(values[1]), int(values[2])))

        new_image = Image.new(Mode, (Width, Height))
        new_image.putdata(pixel_values)
        new_image.save(output_image_path)

    def __update_csv_value(self, file_path, row_position_table, new_value_table):
        updated_rows = []
        with open(file_path, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            position = 0
            for i, row in enumerate(csvreader, start=1):
                if i != row_position_table[position]:
                    updated_rows.append(row)
                elif i == row_position_table[position]:
                    updated_rows.append(new_value_table[position])
                    if position < len(row_position_table) - 1:
                        position += 1

        with open(file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(updated_rows)

    def encode_image(self, key, filecsv, image, text):
        cdmess, key = self.__get_coded_message(text=text, key=key)
        gen = self.__csv_row_generator(filecsv)
        self.__putting_pixels_value_into_file(image, filecsv)
        chunked_cdmess = [cdmess[i:i+7] for i in range(0, len(cdmess), 7)]
        result = ' '.join(chunked_cdmess)
        print(result)
        length_of_key = len(key)
        length_of_message = len(result)
        y = 1
        list = []
        row_point = 0
        for x in key:
            row_point += int(x, 16)
        which_lines = []
        what_value = []
        for x in range(length_of_message-1):
            coding_value = (x + 1)**2
            row_value = self.__get_csv_row(gen, row_point)
            one_of_rgb_value = int(row_value[int(key[coding_value % length_of_key]) % 3])   
            list.append(str(key[coding_value % length_of_key]))    
            if y % 8 == 0:
                if y == length_of_message:
                    if one_of_rgb_value % 2 == 0:
                        if one_of_rgb_value == 0:
                            one_of_rgb_value += 1
                        elif one_of_rgb_value == 255:
                            one_of_rgb_value -= 1
                        else:
                            one_of_rgb_value += 1
                        which_lines.append(row_point)
                        row_value[int(key[coding_value % length_of_key]) % 3] = str(one_of_rgb_value)
                        what_value.append(row_value)
                elif y != length_of_message:
                    if one_of_rgb_value % 2 == 1:
                        if one_of_rgb_value == 0:
                            one_of_rgb_value += 1
                        elif one_of_rgb_value == 255:
                            one_of_rgb_value -= 1
                        else:
                            one_of_rgb_value += 1
                        which_lines.append(row_point)
                        row_value[int(key[coding_value % length_of_key]) % 3] = str(one_of_rgb_value)
                        what_value.append(row_value) 
            else:
                if int(result[x]) == 0:
                    if one_of_rgb_value % 2 == 1:
                        if one_of_rgb_value == 0:
                            one_of_rgb_value += 1
                        elif one_of_rgb_value == 255:
                            one_of_rgb_value -= 1
                        else:
                            one_of_rgb_value += 1
                        which_lines.append(row_point)
                        row_value[int(key[coding_value % length_of_key]) % 3] = str(one_of_rgb_value)
                        what_value.append(row_value)
                elif int(result[x]) == 1:
                    if one_of_rgb_value % 2 == 0:
                        if one_of_rgb_value == 0:
                            one_of_rgb_value += 1
                        elif one_of_rgb_value == 255:
                            one_of_rgb_value -= 1
                        else:
                            one_of_rgb_value += 1
                        which_lines.append(row_point)
                        row_value[int(key[coding_value % length_of_key]) % 3] = str(one_of_rgb_value)
                        what_value.append(row_value)
            y += 1
            row_point += int(key[coding_value % length_of_key])
        self.__update_csv_value(filecsv, which_lines, what_value)
        self.__create_image_from_csv(filecsv, f"{ROOT_DIR}/images/coded_image.png")
        print(list)

    def decode_image(self, key, filecsv, image):
        self.__putting_pixels_value_into_file(image, filecsv)
        gen = self.__csv_row_generator(filecsv)
        length_of_key = len(key)
        list = []
        bin_value = ''
        row_point = 0
        coding_value = 0
        x = 0
        y = 1
        end = 0
        for i in key:
            row_point += int(i, 16)
        while end == 0:
            coding_value = (x + 1)**2
            row_value = self.__get_csv_row(gen, row_point)
            one_of_rgb_value = int(row_value[int(key[coding_value % length_of_key]) % 3])
            list.append(str(key[coding_value % length_of_key]))
            if y % 8 == 0:
                if one_of_rgb_value % 2 == 1:
                    end = 1
                else:
                    bin_value += ' '
            else:
                if one_of_rgb_value % 2 == 0:
                    bin_value += '0'
                else:
                    bin_value += '1'
            row_point += int(key[coding_value % length_of_key])
            y += 1
            x += 1
        print(list)
        return bin_value


if __name__ == "__main__":
    to = image_stenographing()
    to.encode_image(
                    key="432412421",
                    filecsv=f"{ROOT_DIR}/resources/precoded_pixels.csv",
                    image=f"{ROOT_DIR}/images/png2.png",
                    text="Random text"
                    )
    bin_value = to.decode_image(
                    key="432412421",
                    filecsv=f"{ROOT_DIR}/resources/plik.csv",
                    image=f"{ROOT_DIR}/images/coded_image.png"
                    )
    print(bin_value)