import os
from PIL import Image
import csv
from obfuscateText import TextObfuscator as txob

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


class image_stenographing():
    Width = 0
    Height = 0
    Mode = ''

    def __init__(self):
        self.obfs = txob()

    def __get_coded_message(self, text, key):
        return self.obfs.obfuscate(text=text, key=key)

    def __putting_pixels_value_into_file(self, photo, filecsv):
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
        for i, row in enumerate(generator):
            if i == target_row:
                return row
    
    def __create_image_from_csv(self, csv_file_path, output_image_path):
        pixel_values = []

        with open(csv_file_path, 'r') as csvfile:
            csvreader = csvfile.readlines()
            for line in csvreader:
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
            for i, row in enumerate(csvreader):
                if i != row_position_table[position]:
                    updated_rows.append(row)
                elif i == row_position_table[position]:
                    updated_rows.append(new_value_table[position])
                    if position < len(row_position_table)-1:
                        position += 1

        with open(file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(updated_rows)

    def encode_image(self, key, filecsv, image, text):
        cdmess, key = self.__get_coded_message(text=text, key=key)
        gen = self.__csv_row_generator(filecsv)
        self.__putting_pixels_value_into_file(image, filecsv)
        if len(cdmess) % 8 == 0:
            chunked_cdmess = [cdmess[i:i+7] for i in range(0, len(cdmess), 8)]
            result = ' '.join(chunked_cdmess)
        else:  
            chunked_cdmess = [cdmess[i:i+8] for i in range(0, len(cdmess), 8)]
            result = ' '.join(chunked_cdmess)
            result += ' '
        length_of_key = len(key)
        length_of_message = len(result)
        sum = 0
        for x in key:
            sum += int(x)
        row_point = sum 
        which_lines = []
        what_value = []
        for x in range(length_of_message-1):
            row_value = self.__get_csv_row(gen, row_point)
            row_point += int(key[x % length_of_key])
            one_of_rgb_value = int(row_value[int(key[x % length_of_key]) % 3])
            if x % 9 == 0:
                if x == length_of_message-1:
                    if one_of_rgb_value % 2 == 0:
                        if one_of_rgb_value == 0:
                            one_of_rgb_value += 1
                        elif one_of_rgb_value == 255:
                            one_of_rgb_value -= 1
                        else:
                            one_of_rgb_value += 1
                        which_lines.append(row_point)
                        row_value[int(key[x % length_of_key]) % 3] = str(one_of_rgb_value)
                        what_value.append(row_value)
                elif x != length_of_message-1:
                    if one_of_rgb_value % 2 == 1:
                        if one_of_rgb_value == 0:
                            one_of_rgb_value += 1
                        elif one_of_rgb_value == 255:
                            one_of_rgb_value -= 1
                        else:
                            one_of_rgb_value += 1
                        which_lines.append(row_point)
                        row_value[int(key[x % length_of_key]) % 3] = str(one_of_rgb_value)
                        what_value.append(row_value) 

            elif x % 9 != 0:
                if int(cdmess[x]) == 0:
                    if one_of_rgb_value % 2 == 1:
                        if one_of_rgb_value == 0:
                            one_of_rgb_value += 1
                        elif one_of_rgb_value == 255:
                            one_of_rgb_value -= 1
                        else:
                            one_of_rgb_value += 1
                        which_lines.append(row_point)
                        row_value[int(key[x % length_of_key]) % 3] = str(one_of_rgb_value)
                        what_value.append(row_value)
                elif int(cdmess[x]) == 1:
                    if one_of_rgb_value % 2 == 0:
                        if one_of_rgb_value == 0:
                            one_of_rgb_value += 1
                        elif one_of_rgb_value == 255:
                            one_of_rgb_value -= 1
                        else:
                            one_of_rgb_value += 1
                        which_lines.append(row_point)
                        row_value[int(key[x % length_of_key]) % 3] = str(one_of_rgb_value)
                        what_value.append(row_value)
        self.__update_csv_value(filecsv, which_lines, what_value)
        self.__create_image_from_csv(filecsv, f"{ROOT_DIR}/resources/images/coded_image.png")

    # def decode_image(self, key, filecsv, image):
    #     self.__putting_pixels_value_into_file(image, filecsv)
    #     gen = self.__csv_row_generator(filecsv)
    #     self.__putting_pixels_value_into_file(image, filecsv)
    #     length_of_key = len(key)
    #     bin_value = ''
    #     sum = 0
    #     for x in key:
    #         sum += int(x)
    #     row_point = sum
    #     which_lines = []
    #     what_value = []
    #     for x in key:
    #         row_value = self.__get_csv_row(gen, row_point)
    #         row_point += int(x)
    #         r_or_g_or_b = int(key[x % length_of_key]) % 3
    #         if int(row_value[r_or_g_or_b]) % 2 == 0:
    #             if one_of_rgb_value % 2 == 1:
    #                 if one_of_rgb_value == 0:
    #                     one_of_rgb_value += 1
    #                     which_lines.append(row_point)
    #                     row_value[int(key[x % length_of_key]) % 3] = str(one_of_rgb_value)
    #                     what_value.append(row_value)
    #                 elif one_of_rgb_value == 255:
    #                     one_of_rgb_value -= 1
    #                     which_lines.append(row_point)
    #                     row_value[int(key[x % length_of_key]) % 3] = str(one_of_rgb_value)
    #                     what_value.append(row_value)
    #                 else:
    #                     one_of_rgb_value += 1
    #                     which_lines.append(row_point)
    #                     row_value[int(key[x % length_of_key]) % 3] = str(one_of_rgb_value)
    #                     what_value.append(row_value)
    #         elif int(cdmess[x]) == 1:
    #             if one_of_rgb_value % 2 == 0:
    #                 if one_of_rgb_value == 0:
    #                     one_of_rgb_value += 1
    #                     which_lines.append(row_point)
    #                     row_value[int(key[x % length_of_key]) % 3] = str(one_of_rgb_value)
    #                     what_value.append(row_value)
    #                 elif one_of_rgb_value == 255:
    #                     one_of_rgb_value -= 1
    #                     which_lines.append(row_point)
    #                     row_value[int(key[x % length_of_key]) % 3] = str(one_of_rgb_value)
    #                     what_value.append(row_value)
    #                 else:
    #                     one_of_rgb_value += 1
    #                     which_lines.append(row_point)
    #                     row_value[int(key[x % length_of_key]) % 3] = str(one_of_rgb_value)
    #                     what_value.append(row_value)
            
    #     self.__update_csv_value(filecsv, which_lines, what_value)
    #     self.__create_image_from_csv(filecsv, "coded_photo.png")
        


if __name__ == "__main__":
    to = image_stenographing()
    to.encode_image(
                    key="432412421",
                    filecsv=f"{ROOT_DIR}/resources/precoded_pixels.csv",
                    image=f"{ROOT_DIR}/resources/images/png2.png", 
                    text="Random text"
                    )
    # to.decode_image(
    #                 key="432412421", 
    #                 filecsv="new_file.csv",
    #                 image="coded_photo.png"
    #                 )
