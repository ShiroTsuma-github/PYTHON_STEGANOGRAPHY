import tkinter as tk
import os
from PIL import ImageTk, Image
import generateEncodingKey as gek
from datetime import datetime
key = gek.GenerateKey(36, 'hex')

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


def encoding():
    output_text_field.insert(tk.END, f'[{datetime.now().strftime("%H:%M:%S")}]: Image encoded\n')
    output_text_field.insert(tk.END, input_text_field.get(1.0, tk.END))


def decoding():
    output_text_field.delete(1.0, tk.END)
    output_text_field.insert(tk.END, f'[{datetime.now().strftime("%H:%M:%S")}]: Image decoded\n')
    output_text_field.insert(tk.END, f'Decoded text...\n')


def getting_image():
    print("Getting image...")

def creating_encoded_key():
    currentDateAndTime = datetime.now().strftime("%H:%M:%S")
    key_crypting_text_field.delete(1.0, tk.END)
    key_crypting_text_field.insert(tk.END, next(key))
    # output_text_field.delete(1.0, tk.END)
    output_text_field.insert(tk.END, f'[{currentDateAndTime}]: Key generated\n')

def making_image_usable()

root = tk.Tk()
root.title("Stenography App")

# Set the size of the window
window_width = 700
window_height = 640
root.geometry(f"{window_width}x{window_height}")

# Calculate the position of the window to center it on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
# Set the position of the window
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.resizable(False, False)

photo_frame = tk.LabelFrame(root, bd=3, relief=tk.GROOVE, width=400, height=300)
photo_frame.grid(row=0, column=0, pady=5)

buttons_frame = tk.LabelFrame(root, bd=3, relief=tk.GROOVE, width=400, height=300)
buttons_frame.grid(row=0, column=1, pady=5)

input_output_frame = tk.LabelFrame(root, bd=3, relief=tk.GROOVE, width=680, height=150)
input_output_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

encode_button = tk.Button(buttons_frame, text="Encode", command=encoding, width=38, height=4)
encode_button.grid(row=0, column=0, pady=20, padx=5)

decode_button = tk.Button(buttons_frame, text="Decode", command=decoding, width=38, height=4)
decode_button.grid(row=1, column=0, pady=20, padx=5)


frame_for_encryption_key = tk.LabelFrame(buttons_frame, bd=0, relief=tk.GROOVE,)
frame_for_encryption_key.grid(row=2, column=0, padx=5, pady=10)

label_for_crypting_key = tk.Label(frame_for_encryption_key, text="Encryption key: ")
label_for_crypting_key.grid(row=2, column=0, columnspan=2)

key_crypting_text_field = tk.Text(frame_for_encryption_key, width=30, height=2)
key_crypting_text_field.grid(row=3, column=0, padx=5)

image2 = Image.open(f"{ROOT_DIR}/resources/images/randomize.png")
new_image2 = image2.resize((28, 28))
test2 = ImageTk.PhotoImage(new_image2)

creating_key_button = tk.Button(frame_for_encryption_key, width=28, height=28, image=test2, command=creating_encoded_key)
creating_key_button.grid(row=3, column=1, padx=5)

label_for_input_field = tk.Label(input_output_frame, text="Input data:")
label_for_input_field.grid(row=0, padx=10, pady=2)

input_text_field = tk.Text(input_output_frame, width=82, height=4)
input_text_field.grid(row=1, padx=10, pady=5)

label_for_output_field = tk.Label(input_output_frame, text="Output data:")
label_for_output_field.grid(row=2, padx=10, pady=2)

output_text_field = tk.Text(input_output_frame, width=82, height=10)
output_text_field.grid(row=3, padx=10, pady=5)

image1 = Image.open(f"{ROOT_DIR}/resources/images/png2.png")
new_image = image1.resize((370, 290))
test = ImageTk.PhotoImage(new_image)

image_getting_button = tk.Button(photo_frame, image=test, command=getting_image)
image_getting_button.grid(row=0, column=0, sticky="nsew")



root.mainloop()
