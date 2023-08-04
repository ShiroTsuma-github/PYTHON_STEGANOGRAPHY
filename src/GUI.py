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

photo_frame = tk.Frame(root, borderwidt=1, relief=tk.GROOVE, padx=180, pady=135)
photo_frame.pack(side=tk.LEFT, padx=10, pady=10)

buttons_frame = tk.Frame(root, borderwidt=1, relief=tk.GROOVE, padx=130, pady=85)
buttons_frame.pack(side=tk.RIGHT, padx=10, pady=10)

encode_button = tk.Button(buttons_frame, text="Encode", command=encoding, padx=50, pady=50)
encode_button.grid(row=1, column=2, padx=10, pady=10)

decode_button = tk.Button(buttons_frame, text="Decode", command=decoding, padx=10, pady=10)

key_crypting_text_field = tk.Entry(buttons_frame) 

image_label = tk.Label(photo_frame, text="there will be photo")
image_label.grid(row=1, column=2)
root.mainloop()
