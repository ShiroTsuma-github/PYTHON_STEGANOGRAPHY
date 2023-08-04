import customtkinter
import tkinter as tk
import os
from PIL import Image

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


class Button_Frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.encode = customtkinter.CTkButton(self, text="Encode", command=self.encode_callback)
        self.encode.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew", columnspan=2)
        self.decode = customtkinter.CTkButton(self, text="Decode", command=self.decode_callback)
        self.decode.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew", columnspan=2)
        self.key_frame = Randomise_Space(self)
        self.key_frame.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nsew")

    def encode_callback(self):
        print("encode pressed")

    def decode_callback(self):
        print("decode pressed")


class Randomise_Space(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.randomise_image = customtkinter.CTkImage(Image.open("resources/images/random.png"), size=(25, 25))
        self.rowconfigure(0, weight=2)
        self.key_input = customtkinter.CTkEntry(self)
        self.key_input.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.randomise_image = tk.PhotoImage(file="resources/images/random.png",
                                             width=25,
                                             height=25)
        self.randomise_button = customtkinter.CTkButton(self,
                                                        text="",
                                                        image=self.randomise_image,
                                                        command=self.random_key_callback,
                                                        width=30,
                                                        height=self.key_input.cget("height"))
        self.randomise_button.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

    def random_key_callback(self):
        print("random key pressed")


class InputOutputFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(0, weight=2)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=5)
        self.input_field = customtkinter.CTkEntry(self)
        self.input_field.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.output_field = customtkinter.CTkEntry(self)
        self.output_field.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("640x640")
        # self.resizable(False, False)
        self.rowconfigure(1, weight=2)
        self.columnconfigure(1, weight=1)
        self.photo_image = customtkinter.CTkImage(Image.open("resources/images/png1.png"), size=(370, 290))


        self.image_frame = customtkinter.CTkFrame(self)
        self.image_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nswe")
        self.image = customtkinter.CTkLabel(self.image_frame,text='', image=self.photo_image)
        self.image.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
        self.button_frame = Button_Frame(self)
        self.button_frame.grid(row=0, column=1,padx=(0, 10), pady=(10, 0), sticky="nsew")

        self.input_output_frame = InputOutputFrame(self)
        self.input_output_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    

    def button_callback(self):
        print("button pressed")



app = App()
app.mainloop()