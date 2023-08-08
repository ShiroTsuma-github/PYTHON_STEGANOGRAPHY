from typing import Optional, Tuple, Union
import customtkinter as ctk
import tkinter as tk
import tkinter.filedialog
from PIL import Image
import sys
import os


ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from src.generateEncodingKey import GenerateKey  # noqa: E402


class ImageFrame(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.image = None
        self.c_font = ("Impact", 16)
        self.btn_choose = ctk.CTkButton(self,
                                        height=70,
                                        text="Choose Image",
                                        font=self.c_font,
                                        command=self.choose_img)
        self.btn_choose.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nswe")
        self.btn_choose.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def choose_img(self) -> None:
        infile: str = tk.filedialog.askopenfilename(
            initialdir=f'{ROOT_DIR}/resources/images',
            title="Select file")
        if not infile:
            return
        self.image = ctk.CTkImage(Image.open(infile), size=(350, 270))
        self.btn_choose.configure(image=self.image,
                                  height=370,
                                  width=290,
                                  text="",
                                  fg_color='transparent',
                                  hover=False)
        self.grid(row=0, column=0, padx=(0, 10), pady=(10, 0), sticky="nswe")
        self.btn_choose.image = self.image

    def clear_img(self):
        self.btn_choose.configure(image=None,
                                  height=70,
                                  text="Choose Image",
                                  hover=True,
                                  fg_color=('#3B8ED0', '#1F6AA5'))
        self.btn_choose.image = None


class ButtonFrame(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.master = master
        self.columnconfigure(0, weight=1)
        self.b_font = ("Impact", 26)
        self.t_font = ("Impact", 16)
        self.btn_encode = ctk.CTkButton(self,
                                        text="Encode",
                                        height=50,
                                        font=self.b_font,
                                        command=self.encode)
        self.btn_encode.grid(row=0, column=0, padx=(10, 10), pady=(10, 0), sticky="nswe")
        self.btn_decode = ctk.CTkButton(self,
                                        text="Decode",
                                        height=50,
                                        font=self.b_font,
                                        command=self.decode)
        self.btn_decode.grid(row=1, column=0, padx=(10, 10), pady=(10, 0), sticky="nswe")
        self.key_input = ctk.CTkEntry(self, height=40, font=self.t_font)
        self.key_input.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.key_frame = KeyFrame(self)
        self.key_frame.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="nsew")

    def encode(self) -> None:
        pass

    def decode(self) -> None:
        pass


class KeyFrame(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.master = master
        self.rowconfigure(0, weight=1)
        self.key_gen = GenerateKey(format='hex', key_length=31)
        self.img_random = ctk.CTkImage(
            Image.open(f"{ROOT_DIR}/resources/images/random.png"),
            size=(30, 30))
        self.img_copy = ctk.CTkImage(
            Image.open(f"{ROOT_DIR}/resources/images/copy.png"),
            size=(25, 25))
        self.img_clear = ctk.CTkImage(
            Image.open(f"{ROOT_DIR}/resources/images/clear.png"),
            size=(35, 35))
        self.btn_clear = ctk.CTkButton(self,
                                       text="",
                                       image=self.img_clear,
                                       width=75,
                                       height=23,
                                       command=self.clear)
        self.btn_clear.grid(row=0, column=0, padx=(10, 5), pady=(10, 10), sticky="nsew")
        self.btn_copy = ctk.CTkButton(self,
                                      text="",
                                      width=75,
                                      height=23,
                                      image=self.img_copy,
                                      command=self.copy)
        self.btn_copy.grid(row=0, column=1, padx=5, pady=(10, 10), sticky="nsew")
        self.btn_generate = ctk.CTkButton(self,
                                          text="",
                                          image=self.img_random,
                                          width=75,
                                          height=23,
                                          command=self.generate_key)
        self.btn_generate.grid(row=0, column=2, padx=(5, 10), pady=(10, 10), sticky="nsew")

    def generate_key(self) -> None:
        key = next(self.key_gen)
        self.master.key_input.delete(0, tk.END)
        self.master.key_input.insert(0, key)

    def clear(self) -> None:
        self.master.key_input.delete(0, tk.END)
        self.master.master.clear_image()

    def copy(self) -> None:
        self.clipboard_clear()
        self.clipboard_append(self.master.key_input.get())


class DataFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.columnconfigure(0, weight=2)
        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=2)
        self.t_font = ("Impact", 18)
        self.input_field = ctk.CTkTextbox(self, font=self.t_font)
        self.input_field.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.output_field = ctk.CTkTextbox(self, font=self.t_font)
        self.output_field.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")

    def getting_input(self):
        return self.input_field.get("1.0", tk.END)

    def put_into_output(self, text):
        self.output_field.insert("1.0", text=text)


class AuthorsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.b_font = ("Impact", 18)
        self.lbl_authors = ctk.CTkLabel(self,
                                        text="Authors:\tTomasz Góralski\tHubert Przewoźniak",
                                        font=self.b_font)
        self.lbl_authors.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Steganography")
        self.geometry("640x640")
        self.resizable(False, False)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=2)

        self.image_frame = ImageFrame(self)
        self.image_frame.grid(row=0, column=0, padx=(0, 10),ipadx=65, pady=(10, 0), sticky="nswe")
        self.button_frame = ButtonFrame(self)
        self.button_frame.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="nsew")
        self.data_frame = DataFrame(self)
        self.data_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.authors_frame = AuthorsFrame(self)
        self.authors_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

    def clear_image(self):
        self.image_frame.clear_img()


if __name__ == "__main__":
    app = App()
    app.mainloop()

