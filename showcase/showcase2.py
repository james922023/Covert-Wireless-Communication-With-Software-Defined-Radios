import cv2
import random
import numpy as np
from tkinter import Tk, Label, Button, Entry, Text
from tkinter import messagebox
from PIL import Image, ImageTk


def load_image(path, grayscale=True):
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Could not load image from the path: {path}")
    return image


def generate_key_sequence(seed, length):
    random.seed(seed)
    sequence = list(range(length))
    random.shuffle(sequence)
    return sequence


def binary_to_image(binary_data, shape):
    pixels = [int(binary_data[i:i + 8], 2) for i in range(0, len(binary_data), 8)]
    return np.array(pixels, dtype=np.uint8).reshape(shape)


def extract_message(stego_image, msg_length, key):
    height, width = stego_image.shape
    pixels_count = height * width
    key_sequence = generate_key_sequence(key, pixels_count)
    
    binary_message = ''
    for i in range(msg_length * 8):  # 8 bits for each character
        pixel_idx = key_sequence[i]
        x, y = divmod(pixel_idx, width)
        bit = stego_image[x, y] & 1
        binary_message += str(bit)
    
    message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))
    return message


def extract_image(stego_image, shape, key):
    height, width = stego_image.shape
    pixels_count = height * width
    key_sequence = generate_key_sequence(key, pixels_count)
    
    binary_hidden_image = ''
    for i in range(shape[0] * shape[1] * 8):
        pixel_idx = key_sequence[i]
        x, y = divmod(pixel_idx, width)
        bit = stego_image[x, y] & 1
        binary_hidden_image += str(bit)
    
    return binary_to_image(binary_hidden_image, shape)


class StegoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Message and Image Extractor")
        self.root.geometry("800x700")
        root.configure(bg="#1E1E1E")  # Set background color
        
        # UI Elements (From the second code)
        self.label = Label(root, text="Enter the name of the Stego Image", font=("Arial", 12), bg="#2A2A2A", fg="#E0E0E0")  
        self.label.pack(pady=10)

        self.filepath_entry = Entry(root, width=50)
        self.filepath_entry.pack(pady=5)

        self.key_label = Label(root, text="Enter Key phrase for Extraction", font=("Arial", 12), bg="#2A2A2A", fg="#E0E0E0")
        self.key_label.pack(pady=5)

        self.key_entry = Entry(root, width=30)
        self.key_entry.pack(pady=5)

        self.msg_length_label = Label(root, text="Enter Message Length (only if extracting message)", font=("Arial", 12), bg="#2A2A2A", fg="#E0E0E0")
        self.msg_length_label.pack(pady=5)

        self.msg_length_entry = Entry(root, width=30)
        self.msg_length_entry.pack(pady=5)

        self.extract_button = Button(root, text="Extract", command=self.extract_data, bg="#3D3D3D", fg="#E0E0E0")
        self.extract_button.pack(pady=10)

        self.result_label = Label(root, text="Extracted message/image:", font=("Arial", 12), bg="#2A2A2A", fg="#E0E0E0")
        self.result_label.pack(pady=10)

        self.canvas = None

    def extract_data(self):
        try:
            # Get values from user inputs
            key = int(self.key_entry.get())
            if self.msg_length_entry.get():
                msg_length = int(self.msg_length_entry.get())
            else:
                msg_length = None
            filepath = self.filepath_entry.get()

            # Load the image using the filepath entered by the user
            stego_image = load_image(filepath)

            if msg_length:  # Extract hidden message
                extracted_message = extract_message(stego_image, msg_length, key)
                self.display_message(extracted_message)
            else:  # Extract hidden image
                hidden_image_shape = (128, 128)  # Example shape
                extracted_image = extract_image(stego_image, hidden_image_shape, key)
                self.display_image(extracted_image)
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def display_message(self, message):
        self.result_label.config(text="Extracted Message:")
        text_box = Text(self.root, height=10, width=50)
        text_box.insert("1.0", message)
        text_box.pack(pady=10)

    def display_image(self, image_data):
        image = Image.fromarray(image_data)

        width, height = image.size
        max_size = 400  

        if width > height:
            new_width = max_size
            new_height = int((new_width / width) * height)
        else:
            new_height = max_size
            new_width = int((new_height / height) * width)

        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)  
        self.display_image_on_canvas(image)

    def display_image_on_canvas(self, image):
        if self.canvas:
            self.canvas.destroy()

        self.canvas = Label(self.root)
        self.canvas.image = ImageTk.PhotoImage(image)
        self.canvas.config(image=self.canvas.image)
        self.canvas.pack(pady=10)


root = Tk()
gui = StegoGUI(root)
root.mainloop()
