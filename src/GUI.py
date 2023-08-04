import tkinter as tk
import os
from PIL import ImageTk, Image

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


def encoding():
    print("Image encoded")


def decoding():
    print("Image decoded")


def getting_image():
    print("Image downloaded")


root = tk.Tk()
root.title("Stenography App")

# Set the size of the window
window_width = 640
window_height = 480
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
photo_frame.grid(row=0, column=0, padx=5, pady=5)

buttons_frame = tk.LabelFrame(root, bd=3, relief=tk.GROOVE, width=210, height=300)
buttons_frame.grid(row=0, column=1, padx=5, pady=5)

input_output_frame = tk.LabelFrame(root, bd=3, relief=tk.GROOVE, width=620, height=150)
input_output_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

#encode_button = tk.Button(buttons_frame, text="Encode", command=encoding)
#encode_button.pack()

#decode_button = tk.Button(buttons_frame, text="Decode", command=decoding)
#decode_button.pack()

#key_crypting_text_field = tk.Entry(buttons_frame)
#key_crypting_text_field.pack()

#input_text_field = tk.Entry(input_output_frame, width=200)
#input_text_field.pack(padx=10, pady=10)

#output_text_field = tk.Entry(input_output_frame, width=300)
#output_text_field.pack(padx=10, pady=10)

image1 = Image.open(f"{ROOT_DIR}/resources/images/img1.jpeg")
new_image = image1.resize((400, 300))
test = ImageTk.PhotoImage(new_image)

image_label = tk.Label(photo_frame, image=test)
image_label.grid(row=0, column=0, sticky="nsew")



root.mainloop()
