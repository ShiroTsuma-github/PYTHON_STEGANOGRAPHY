import sys
import os
import tkinter as tk
import customtkinter as ctk
import tkinter.filedialog
import tkinter.messagebox
from PIL import Image
import json
import deprecation


ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
from src.generateEncodingKey import GenerateKey     # noqa: E402
from src.obfuscateText import TextObfuscator        # noqa: E402
from src.steganographImage import SteganoImage      # noqa: E402


def get_config_path() -> str:
    """Return valid path for app, when run in main.py or exe,
    to allow for permanent settings.

    Returns:
        str: Valid path to use
    """
    if hasattr(sys, "_MEIPASS"):
        abs_home = os.path.abspath(os.path.expanduser("~"))
        abs_dir_app = os.path.join(abs_home, ".Steganograph")
        if not os.path.exists(abs_dir_app):
            os.mkdir(abs_dir_app)
        cfg_path = os.path.join(abs_dir_app, "config.json")
    else:
        cfg_path = os.path.abspath(".%sresources\config.json" % os.sep)
    return cfg_path


def load_json(option: str) -> str | None:
    """Loads config.json, that stores default path to images.

    Args:
        option (str): Setting from json

    Returns:
        str | None: Setting if exists. None if error or it doesn't exist
    """
    config_file_path = get_config_path()
    if os.path.exists(config_file_path):
        try:
            with open(config_file_path, "r") as config_file:
                config = json.load(config_file)
                return config.get(option)
        except:
            return None

    return None


def save_json(option: str, image_directory: str) -> None:
    """Saves setting to json. Based on main.py or .exe location is different.

    Args:
        option (str): Option to overwrite or add
        image_directory (str): Location to add
    """
    path = get_config_path()
    data = {option: image_directory}
    if os.path.exists(path):
        with open(path, "r+") as json_file:
            data = json.load(json_file)
        data.update({option: image_directory})
    with open(path, "w") as config_file:
        json.dump(data, config_file)


class ImageFrame(ctk.CTkFrame):
    """Frame that holds button to choose image and image picker

    Args:
        ctk (CTkFrame): customtkinter container for objects
    """
    def __init__(self, master) -> None:
        super().__init__(master)
        self.image = None
        """Image to display"""
        self.image_path = None
        """Path of image"""
        self.c_font = ("Impact", 16)
        """Font used"""
        self.btn_choose = ctk.CTkButton(self,
                                        height=70,
                                        text="Choose Image",
                                        font=self.c_font,
                                        command=self.choose_img)
        """Button for displaying Image and text. Interactive"""
        self.btn_choose.grid(row=0, column=0, padx=(
            10, 0), pady=(10, 0), sticky="nswe")
        self.btn_choose.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def choose_img(self) -> None:
        """Action after clicking button | Image. Shows filedialog
        """
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
        """Action invoked by pressing Clear button.
        Interface to allow clearing through master"""
        self.btn_choose.configure(image=None,
                                  height=70,
                                  text="Choose Image",
                                  hover=True,
                                  fg_color=('#3B8ED0', '#1F6AA5'))
        self.btn_choose.image = None

    def get_image_path(self) -> str:
        """Returns image displayed, to be used when getting displayed image

        Returns:
            str: Image displayed
        """
        return self.image_path


class ButtonFrame(ctk.CTkFrame):
    """Frame holding main images and container with icon buttons and key field

    Args:
        ctk (CtkFrame): customtkinter container for objects
    """
    def __init__(self, master) -> None:
        super().__init__(master)
        self.master = master
        """Parent of ButtonFrame"""
        self.columnconfigure(0, weight=1)
        self.b_font = ("Impact", 26)
        """Button big font"""
        self.t_font = ("Impact", 16)
        """Text font"""
        self.btn_encode = ctk.CTkButton(self,
                                        text="Encode",
                                        height=50,
                                        font=self.b_font,
                                        command=self.encode)
        """Button to encode text"""
        self.btn_encode.grid(row=0, column=0, padx=(
            10, 10), pady=(10, 0), sticky="nswe")
        self.btn_decode = ctk.CTkButton(self,
                                        text="Decode",
                                        height=50,
                                        font=self.b_font,
                                        command=self.decode)
        """Button to decode text"""
        self.btn_decode.grid(row=1, column=0, padx=(
            10, 10), pady=(10, 0), sticky="nswe")
        self.key_input = ctk.CTkEntry(self, height=40, font=self.t_font)
        """Key input"""
        self.key_input.grid(row=2, column=0, padx=10,
                            pady=(10, 0), sticky="nsew")
        self.key_frame = KeyFrame(self)
        """Frame holding icon buttons for easier layout"""
        self.key_frame.grid(row=3, column=0, padx=10,
                            pady=(10, 0), sticky="nsew")

    def encode(self) -> None:
        """Encodes and saves image, after text, image and key are picked and valid.
        Shows errors before that and after everything is valid it shows file save dialog
        """
        to = TextObfuscator()
        text: str = self.master.get_input()
        key: str = self.key_input.get()
        image_path = self.master.get_img()
        if not key:
            tk.messagebox.showerror("Error", "Please enter a key")
            return
        if not all([i in '0123456789abcdef' for i in list(key)]):
            tk.messagebox.showerror(
                "Error", "Incorrect key format. (0123456789abcdef)")
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
        """Decodes image and displays decoded content, after image and key are valid
        """
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
            tk.messagebox.showerror(
                "Error", "Incorrect key format. (0123456789abcdef)")
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
    """Frame for icon buttons for easier layout

    Args:
        ctk (CTkFrame): customtkinter container for objects
    """
    def __init__(self, master) -> None:
        super().__init__(master)
        self.master = master
        """ButtonFrame is master"""
        self.rowconfigure(0, weight=1)
        self.key_gen = GenerateKey(format='hex', key_length=31)
        """Button to generate random key"""
        self.img_random = ctk.CTkImage(
            Image.open(f"{ROOT_DIR}/resources/images/random.png"),
            size=(30, 30))
        """Icon for button random"""
        self.img_copy = ctk.CTkImage(
            Image.open(f"{ROOT_DIR}/resources/images/copy.png"),
            size=(25, 25))
        """Icon for button copy"""
        self.img_clear = ctk.CTkImage(
            Image.open(f"{ROOT_DIR}/resources/images/clear.png"),
            size=(35, 35))
        """Icon for button clear"""
        self.btn_clear = ctk.CTkButton(self,
                                       text="",
                                       image=self.img_clear,
                                       width=75,
                                       height=23,
                                       command=self.clear)
        """Clear button"""
        self.btn_clear.grid(row=0, column=0, padx=(10, 5),
                            pady=(10, 10), sticky="nsew")
        self.btn_copy = ctk.CTkButton(self,
                                      text="",
                                      width=75,
                                      height=23,
                                      image=self.img_copy,
                                      command=self.copy)
        """Copy button"""
        self.btn_copy.grid(row=0, column=1, padx=5,
                           pady=(10, 10), sticky="nsew")
        self.btn_generate = ctk.CTkButton(self,
                                          text="",
                                          image=self.img_random,
                                          width=75,
                                          height=23,
                                          command=self.generate_key)
        """Generate Key button"""
        self.btn_generate.grid(row=0, column=2, padx=(
            5, 10), pady=(10, 10), sticky="nsew")

    def generate_key(self) -> None:
        """Generates random preconfigured key and inserts in key input field
        """
        key = next(self.key_gen)
        self.master.key_input.delete(0, tk.END)
        self.master.key_input.insert(0, key)

    def clear(self) -> None:
        """Clears output, image displayed and key field
        """
        self.master.key_input.delete(0, tk.END)
        self.master.master.clear_image()
        self.master.master.clear_output()

    def copy(self) -> None:
        """Copies key to clipboard
        """
        self.clipboard_clear()
        self.clipboard_append(self.master.key_input.get())


class DataFrame(ctk.CTkFrame):
    """Frame for input and output fields

    Args:
        ctk (CTkFrame): customtkinter container for objects
    """
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        """Parent of container"""
        self.columnconfigure(0, weight=2)
        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=2)
        self.t_font = ("Impact", 18)
        """Text field font"""
        self.input_field = ctk.CTkTextbox(self, font=self.t_font)
        """Field for inputting text to encode"""
        self.input_field.grid(row=0, column=0, padx=10,
                              pady=(10, 0), sticky="nsew")
        self.output_field = ctk.CTkTextbox(
            self, font=self.t_font, state='disabled')
        """Output field. Displays results of processes"""
        self.output_field.grid(row=1, column=0, padx=10,
                               pady=(10, 0), sticky="nsew")

    def get_input(self) -> str:
        """Interface to get input easier in parent

        Returns:
            str: Content of input field
        """
        return self.input_field.get("1.0", tk.END)

    def put_into_output(self, text: str) -> None:
        """Puts text into output field and disables it again.

        Args:
            text (str): Message to display
        """
        self.output_field.configure(state="normal")
        self.output_field.insert(tk.END, text=text)
        self.output_field.configure(state="disabled")

    def clear_output(self) -> None:
        """Removes text from output"""
        self.output_field.configure(state="normal")
        self.output_field.delete("1.0", tk.END)
        self.output_field.configure(state="disabled")

    @deprecation.deprecated(deprecated_in="1.0.0.0", details="Due to some problems it doesn't toggle state")
    def toggle_input(self, state) -> None:
        if state:
            self.input_field.configure(state=state)
            return
        state = self.input_field.cget('state')
        if state == 'disabled':
            state = 'normal'
        else:
            state = 'disabled'
        self.input_field.configure(state=state)

    @deprecation.deprecated(deprecated_in="1.0.0.0", details="Due to some problems it doesn't toggle state")
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
    """Footer with authors information

    Args:
        ctk (CTkFrame): customtkinter container for objects
    """
    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.b_font = ("Impact", 18)
        """Font of label"""
        self.lbl_authors = ctk.CTkLabel(self,
                                        text="Authors:\tTomasz Góralski\tHubert Przewoźniak",
                                        font=self.b_font)
        """Information about authors"""
        self.lbl_authors.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


class App(ctk.CTk):
    """Startpoint of application. It hosts most of containers

    Args:
        ctk (CTkFrame): customtkinter container for objects
    """
    def __init__(self):
        super().__init__()
        self.title("Steganography")
        self.geometry("640x640")
        self.resizable(False, False)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=2)

        self.image_frame = ImageFrame(self)
        """Container of image"""
        self.image_frame.grid(row=0, column=0, padx=(
            0, 10), ipadx=65, pady=(10, 0), sticky="nswe")
        self.button_frame = ButtonFrame(self)
        """Container of buttons"""
        self.button_frame.grid(row=0, column=1, padx=(
            0, 10), pady=(10, 0), sticky="nsew")
        self.data_frame = DataFrame(self)
        """Container for input and output"""
        self.data_frame.grid(row=1, column=0, columnspan=2,
                             padx=10, pady=10, sticky="nsew")
        self.authors_frame = AuthorsFrame(self)
        self.authors_frame.grid(
            row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

    def clear_image(self):
        """Forwards image clearing from children to image frame"""
        self.image_frame.clear_img()

    def get_input(self) -> str:
        """Forwards input from data frame to children

        Returns:
            str: Content of input field
        """
        return self.data_frame.get_input()

    def put_output(self, text: str) -> None:
        """Forwards text from children to data frame

        Args:
            text (str): Text to display in output field
        """
        self.data_frame.put_into_output(text)

    def clear_output(self):
        """Clears output field in data frame
        """
        self.data_frame.clear_output()

    def get_img(self) -> str:
        """Forwards image path from image frame to children

        Returns:
            str: path of image displayed
        """
        return self.image_frame.get_image_path()

    @deprecation.deprecated(deprecated_in="1.0.0.0", details="Due to some problems with state toggling")
    def toggle_input(self, state=None):
        """Forwards toggle of state of input to desired or opposite if state is not provided

        Args:
            state (str, optional): State wanted. `disabled` or `normal`. Defaults to None.
        """
        self.data_frame.toggle_input(state)

    @deprecation.deprecated(deprecated_in="1.0.0.0", details="Due to some problems with state toggling")
    def toggle_output(self, state=None):
        """Forwards toggle of state of output to desired or opposite if state is not provided

        Args:
            state (str, optional): State wanted. `disabled` or `normal`. Defaults to None.
        """
        self.data_frame.toggle_output(state)
