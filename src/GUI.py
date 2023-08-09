import customtkinter as ctk
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
from PIL import Image
import sys
import os
import json


ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from src.generateEncodingKey import GenerateKey     # noqa: E402
from src.obfuscateText import TextObfuscator        # noqa: E402
from src.steganographImage import SteganoImage      # noqa: E402


def get_config_path():
    if hasattr(sys, "_MEIPASS"):
        abs_home = os.path.abspath(os.path.expanduser("~"))
        abs_dir_app = os.path.join(abs_home, ".Steganograph")
        if not os.path.exists(abs_dir_app):
            os.mkdir(abs_dir_app)
        cfg_path = os.path.join(abs_dir_app, "config.json")
    else:
        cfg_path = os.path.abspath(".%sresources\config.json" % os.sep)
    return cfg_path


def load_json(option):
    config_file_path = get_config_path()
    if os.path.exists(config_file_path):
        try:
            with open(config_file_path, "r") as config_file:
                config = json.load(config_file)
                return config.get(option)
        except:
            return None

    return None


def save_json(option, image_directory):
    path = get_config_path()
    data = {option: image_directory}
    if os.path.exists(path):
        with open(path, "r+") as json_file:
            data = json.load(json_file)
        data.update({option: image_directory})
    with open(path, "w") as config_file:
        json.dump(data, config_file)


class ImageFrame(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.image = None
        self.image_path = None
        self.c_font = ("Impact", 16)
        self.btn_choose = ctk.CTkButton(self,
                                        height=70,
                                        text="Choose Image",
                                        font=self.c_font,
                                        command=self.choose_img)
        self.btn_choose.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nswe")
        self.btn_choose.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def choose_img(self) -> None:
        data = [("Image Files", "*.png *.jpg *.JPEG")]
        user_profile = os.path.expanduser("~")
        user_image_directory = load_json("image_load_directory")
        if user_image_directory is None:
            default_image_directory = os.path.join(user_profile, "")
        else:
            default_image_directory = user_image_directory
        infile: str = tk.filedialog.askopenfilename(
            filetypes=data,
            defaultextension=data,
            initialdir=default_image_directory,
            title="Select file")
        if not infile:
            return
        if os.path.dirname(infile) != user_image_directory:
            save_json("image_load_directory", os.path.dirname(infile))
        self.image_path = infile
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

    def get_image_path(self) -> str:
        return self.image_path


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
        to = TextObfuscator()
        text: str = self.master.get_input()
        key: str = self.key_input.get()
        image_path = self.master.get_img()
        if not key:
            tk.messagebox.showerror("Error", "Please enter a key")
            return
        if not all([i in '0123456789abcdef' for i in list(key)]):
            tk.messagebox.showerror("Error", "Incorrect key format. (0123456789abcdef)")
            return
        if text.isspace():
            tk.messagebox.showerror("Error", "Please enter a message")
            return
        if not image_path:
            tk.messagebox.showerror("Error", "Please choose an image")
            return
        result, key = to.obfuscate(text, key)
        self.master.clear_output()
        self.master.put_output('Loading data: 100%\n')
        self.master.put_output('Obfuscating: 100%\n')

        steganograph = SteganoImage()
        user_profile = os.path.expanduser("~")
        user_image_directory = load_json("image_save_directory")
        if user_image_directory is None:
            default_image_directory = os.path.join(user_profile, "")
        else:
            default_image_directory = user_image_directory
        data = [("Image Files", "*.png *.jpg")]
        infile: str = tk.filedialog.asksaveasfilename(
            filetypes=data,
            defaultextension=data,
            initialdir=default_image_directory,
            title="Save as")
        if infile:
            image = steganograph.quick_encode(key, image_path, text)
            image.save(infile)
            if os.path.dirname(infile) != user_image_directory:
                save_json("image_save_directory", os.path.dirname(infile))
            self.master.put_output('Encoding: 100%\n')
        else:
            tk.messagebox.showerror("Error", "File not saved")
            self.master.put_output('Encoding: failed\n')
            return
        self.master.put_output('Binary:\n')
        self.master.put_output(result)
        self.master.put_output('\nKey:\n')
        self.master.put_output(key)
        self.master.put_output('\nWithout Decoding:\n')
        self.master.put_output(to.coded_message_to_string(result))

    def decode(self) -> None:
        to = TextObfuscator()
        key: str = self.key_input.get()
        image_path = self.master.get_img()
        if not key:
            tk.messagebox.showerror("Error", "Please enter a key")
            return
        if not image_path:
            tk.messagebox.showerror("Error", "Please choose an image")
            return
        if not all([i in '0123456789abcdef' for i in list(key)]):
            tk.messagebox.showerror("Error", "Incorrect key format. (0123456789abcdef)")
            return
        steganograph = SteganoImage()
        result_bin = steganograph.quick_decode(key, image_path)
        self.master.clear_output()
        self.master.put_output('Loading data: 100%\n')
        self.master.put_output('Deobfuscating: 100%\n')
        self.master.put_output('Binary:\n')
        self.master.put_output(result_bin)
        answer = to.deobfuscate(result_bin, key)
        self.master.put_output('\nMessage:\n')
        self.master.put_output(answer)
        


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
        self.master.master.clear_output()

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
        self.output_field = ctk.CTkTextbox(self, font=self.t_font, state='disabled')
        self.output_field.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")

    def get_input(self):
        return self.input_field.get("1.0", tk.END)

    def put_into_output(self, text):
        self.output_field.configure(state="normal")
        self.output_field.insert(tk.END, text=text)
        self.output_field.configure(state="disabled")

    def clear_output(self):
        self.output_field.configure(state="normal")
        self.output_field.delete("1.0", tk.END)
        self.output_field.configure(state="disabled")

    def toggle_input(self, state):
        if state:
            self.input_field.configure(state=state)
            return
        state = self.input_field.cget('state')
        if state == 'disabled':
            state = 'normal'
        else:
            state = 'disabled'
        self.input_field.configure(state=state)

    def toggle_output(self, state):
        if state:
            self.input_field.configure(state=state)
            return
        state = self.output_field.cget('state')
        if state == 'disabled':
            state = 'normal'
        else:
            state = 'disabled'
        self.output_field.configure(state=state)


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

    def get_input(self):
        return self.data_frame.get_input()

    def put_output(self, text):
        self.data_frame.put_into_output(text)

    def clear_output(self):
        self.data_frame.clear_output()

    def get_img(self):
        return self.image_frame.get_image_path()

    def toggle_input(self, state=None):
        self.data_frame.toggle_input(state)

    def toggle_output(self, state=None):
        self.data_frame.toggle_output(state)


if __name__ == "__main__":
    app = App()
    app.mainloop()

