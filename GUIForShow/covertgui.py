import tkinter as tk
from PIL import Image, ImageTk
import os
import stego 
import stego2  
import cv2

# Function to update the image display in the GUI
def update_image_display(path, label):
    print(f"Updating image display for path: {path}")  
    if os.path.exists(path):
        image = Image.open(path)
        image_resized = image.resize((300, 300))  
        photo = ImageTk.PhotoImage(image_resized)
        label.config(image=photo)
        label.image = photo 
    else:
        label.config(text="Image Not Found")  

# Function to load the image chosen by the user
def load_image():
    image_path = image_entry.get()  
    if os.path.exists(image_path):
        print(f"Loading image: {image_path}") 
        update_image_display(image_path, original_image_label)
        update_image_display(image_path, stego_image_label)
    else:
        print(f"Image not found: {image_path}")  

# Function for handling the "Hidden txt within image" button
def hidden_txt_within_image():
    hidden_text = text_entry.get() 
    key_phrase = key_phrase_text.get("1.0", "end-1c")  
    print(f"Hidden text: {hidden_text}, Key phrase: {key_phrase}") 
    key = int(key_phrase)
    
    # Get the image path from the user input field
    image_path = image_entry.get()  
    if os.path.exists(image_path):
        image = stego.load_image(image_path)
    
        stego_image = stego.embed_message(image, hidden_text, key)
        print("Message embedded")  
        
        cv2.imwrite("stegomage.png", stego_image)
        print("Message embedded in 'stegomage.png'")
        
        update_image_display("stegomage.png", stego_image_label)
    else:
        print("Original image not found!")

# Function for handling the Hide image within image button
def hide_image_within_image():
    image_name = image_entry.get() 
    hidden_image_name = hidden_image_entry.get() 
    key_phrase = key_phrase_text.get("1.0", "end-1c")
    print(f"Hiding image: {image_name}, Image to hide inside: {hidden_image_name}, Key phrase: {key_phrase}") 
    key = int(key_phrase)  

    # Load the host image
    host_image_path = image_name  
    if os.path.exists(host_image_path):
        host_image = stego2.load_image(host_image_path, grayscale=True)
    else:
        print(f"Host image not found: {host_image_path}")
        return  

    # Load the hidden image to hide within the host image
    hidden_image_path = hidden_image_name  
    if os.path.exists(hidden_image_path):
        hidden_image = stego2.load_image(hidden_image_path, grayscale=True)
    else:
        print(f"Hidden image not found: {hidden_image_path}")
        return

    # Embed the hidden image in the host image
    stego_image = stego2.embed_image(host_image, hidden_image, key)
    print("Hidden image embedded")  

    # Save the stego image as host_with_hidden_image.png
    cv2.imwrite("host.png", stego_image)
    print("Hidden image embedded in 'host.png'")

    # Update the image display for the stego image in the GUI
    update_image_display("host.png", stego_image_label)
    update_image_display(hidden_image_name, original_image_label)


# Main GUI window
root = tk.Tk()
root.title("Image Steganography Display")
root.geometry("800x700")
root.configure(bg="#1E1E1E")  # Set background color

# Image frame
image_frame = tk.Frame(root)
image_frame.pack(pady=10)
image_frame.configure(bg="#1E1E1E")  # Set background color

# Load and display the placeholder image until the user loads a real image
original_image_label = tk.Label(image_frame, text="Original Image", width=300, height=300)
original_image_label.grid(row=0, column=0, padx=10)

stego_image_label = tk.Label(image_frame, text="Steganographed Image", width=300, height=300)
stego_image_label.grid(row=0, column=1, padx=10)

# Initially show 'place.png' as a placeholder image
update_image_display("place.png", original_image_label)
update_image_display("place.png", stego_image_label)

# Create a frame for the input fields and buttons
input_frame = tk.Frame(root, width=600, height=600)
input_frame.pack(pady=20)
input_frame.configure(bg="#2A2A2A")  # Set background color

# Text entry field for entering the name of the image to hide 
image_entry_label = tk.Label(input_frame, text="Enter host image name:",bg="#2A2A2A" , fg="#E0E0E0" , font=("Arial", 9, "bold"))
image_entry_label.grid(row=0, column=0, pady=5)

image_entry = tk.Entry(input_frame, width=30)
image_entry.grid(row=1, column=0, pady=5)

# Load image button, placed next to the text entry field
load_button = tk.Button(input_frame, text="Load Image", width=25, command=load_image,bg="#3D3D3D" , fg="#E0E0E0")
load_button.grid(row=1, column=1, pady=5, padx=10)

# Text entry field for entering text to hide within the image
text_entry_label = tk.Label(input_frame, text="Enter text to hide inside host:",bg="#2A2A2A" , fg="#E0E0E0" , font=("Arial", 9, "bold"))
text_entry_label.grid(row=2, column=0, pady=5)
text_entry = tk.Entry(input_frame, width=30)
text_entry.grid(row=3, column=0, pady=5)

# Text entry field for entering the name of the image to hide inside the host image
hidden_image_label = tk.Label(input_frame, text="Enter image to hide inside host:",bg="#2A2A2A" , fg="#E0E0E0" , font=("Arial", 9, "bold"))
hidden_image_label.grid(row=2, column=1, pady=5)
hidden_image_entry = tk.Entry(input_frame, width=30)
hidden_image_entry.grid(row=3, column=1, pady=5)

# Key phrase input field (spanning both columns)
key_phrase_label = tk.Label(input_frame, text="Enter key phrase:",bg="#2A2A2A" , fg="#E0E0E0" , font=("Arial", 9, "bold"))
key_phrase_label.grid(row=4, column=0, columnspan=2, pady=5)
key_phrase_text = tk.Text(input_frame, width=50, height=3)
key_phrase_text.grid(row=5, column=0, columnspan=2, pady=10)

# Buttons below the key phrase input field
button1 = tk.Button(input_frame, text="Hide text within image", width=25, command=hidden_txt_within_image,bg="#3D3D3D" , fg="#E0E0E0")
button1.grid(row=6, column=0, padx=10, pady=5)

button2 = tk.Button(input_frame, text="Hide image within image", width=25, command=hide_image_within_image , bg="#3D3D3D" , fg="#E0E0E0")
button2.grid(row=6, column=1, padx=10, pady=5)

root.mainloop()
