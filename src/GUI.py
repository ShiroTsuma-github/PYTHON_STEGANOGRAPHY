import tkinter as tk


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

photo_frame = tk.Frame(root,borderwidt=1,relief=tk.GROOVE)
buttons_n_key_input

encode_button = tk.Button(root, text="Encode", command=encoding, padx=50, pady=50)
encode_button.grid(row=1, column=2, padx=10, pady=10)

decode_button = tk.Button(root, text="Decode", command=decoding, padx=10, pady=10)
decode_button.grid(row=2, column=2, padx=10, pady=10)

key_crypting_text_field = tk.Entry(root) 
key_crypting_text_field.grid(row=3, column=2)

image_label = tk.Label(text="there will be photo", padx=180, pady=135)
image_label.grid(row=1,rowspan=3, column=1)

root.mainloop()