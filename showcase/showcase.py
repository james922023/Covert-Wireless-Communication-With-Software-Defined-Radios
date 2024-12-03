import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess
import os
import sys
import io
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

# Redirect stdout and stderr to the Text widget
class RedirectOutput:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.text_widget.configure(state='normal')
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.configure(state='disabled')
    
    def write(self, message):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state='disabled')
    
    def flush(self):
        pass  # Required for Python's logging module

# Function to run a script
def run_script(script_name):
    try:
        process = subprocess.Popen(
            ["python", script_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # Ensures the output is handled as text, not bytes
        )
        # Read and print the output in real-time
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                print(output.strip())
        # Check for errors after the process finishes
        error = process.stderr.read()
        if error:
            print(error.strip())
    except Exception as e:
        print(f"Error running {script_name}: {e}")

# Function to load and display an image
def display_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.gif")])
    if file_path:
        img = Image.open(file_path)
        # Get the size of the right frame
        frame_width = right_frame.winfo_width()
        frame_height = right_frame.winfo_height()

        # Resize the image to fit the frame while maintaining the aspect ratio
        img.thumbnail((frame_width, frame_height))
        img_tk = ImageTk.PhotoImage(img)

        # Update the label with the resized image
        image_label.configure(image=img_tk, text="")
        image_label.image = img_tk

# Create the main window
root = tk.Tk()
root.title("Run Python Scripts")
root.geometry("800x700")
root.configure(bg='#1E1E1E')

# Create a style to change the background color of the tabs
style = ttk.Style()

# Style for the notebook tabs
#style.configure("TNotebook.Tab", background="#1E1E1E", padding=[10, 5])
style.configure("TNotebook", background="#1E1E1E")

# Style for the content of each tab
style.configure("Custom.TFrame", background="#1E1E1E")

# Create a notebook (tabbed interface)
notebook = ttk.Notebook(root, style="TNotebook")  # Apply the TNotebook style here
notebook.pack(fill="both", expand=True)

# First tab (original content)
tab1 = ttk.Frame(notebook, style="Custom.TFrame")
notebook.add(tab1, text="Main Interface")

# Second tab (placeholder for other program)
tab2 = ttk.Frame(notebook, style="Custom.TFrame")
notebook.add(tab2, text="Other Program")

# Main Interface (First Tab)
left_frame = ttk.Frame(tab1, width=400, height=600, style="Custom.TFrame")
left_frame.pack(side="left", fill="both", expand=True)  # Use expand=True to fill space
left_frame.pack_propagate(False)  # Prevent resizing based on content

right_frame = ttk.Frame(tab1, width=400, height=600, style="Custom.TFrame")
right_frame.pack(side="right", fill="both", expand=True)  # Use expand=True to fill space
right_frame.pack_propagate(False)  # Prevent resizing based on content

# Add buttons for scripts
buttons_and_scripts = [
    ("1 Radio Image Transmission", "1023L.py"),
    ("2 Radio Text Transmission", "118t.py"),
    ("2 Radio Image Transmission(WIP)", "notDone.py"),
]

for label, script in buttons_and_scripts:
    button = tk.Button(
        left_frame,
        text=label,
        command=lambda script=script: run_script(script),
        width=30,
        height=2,
        bg="#3D3D3D", fg="#E0E0E0"
        
    )
    button.pack(pady=5)

# Terminal output Text widget
terminal_output = tk.Text(left_frame, wrap="word", height=20, state="disabled", bg="#1E1E1E", fg="#E0E0E0")
terminal_output.pack(padx=10, pady=10, fill="both", expand=True)

# Redirect stdout and stderr
sys.stdout = RedirectOutput(terminal_output)
sys.stderr = RedirectOutput(terminal_output)

# Image display area
image_label = tk.Label(right_frame, text="No Image Loaded", bg="gray", width=50, height=25, anchor="center")
image_label.pack(pady=20, fill="both", expand=True)

# Add a button to load an image
load_image_button = tk.Button(
    right_frame,
    text="Load Image",
    command=display_image,
    width=20,
    height=2
    , bg="#3D3D3D", fg="#E0E0E0"
)
load_image_button.pack(pady=10)

# --- Tab 2 Content ---
# Image frame
image_frame = tk.Frame(tab2)
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
input_frame = tk.Frame(tab2, width=600, height=600)
input_frame.pack(pady=20)
input_frame.configure(bg="#2A2A2A")  # Set background color

# Text entry field for entering the name of the image to hide
image_entry_label = tk.Label(input_frame, text="Enter host image name:", bg="#2A2A2A", fg="#E0E0E0", font=("Arial", 9, "bold"))
image_entry_label.grid(row=0, column=0, pady=5)

image_entry = tk.Entry(input_frame, width=30)
image_entry.grid(row=1, column=0, pady=5)

# Load image button, placed next to the text entry field
load_button = tk.Button(input_frame, text="Load Image", width=25, command=load_image, bg="#3D3D3D", fg="#E0E0E0")
load_button.grid(row=1, column=1, pady=5, padx=10)

# Text entry field for entering text to hide within the image
text_entry_label = tk.Label(input_frame, text="Enter text to hide inside host:", bg="#2A2A2A", fg="#E0E0E0", font=("Arial", 9, "bold"))
text_entry_label.grid(row=2, column=0, pady=5)
text_entry = tk.Entry(input_frame, width=30)
text_entry.grid(row=3, column=0, pady=5)

# Text entry field for entering the name of the image to hide inside the host image
hidden_image_label = tk.Label(input_frame, text="Enter image to hide inside host:", bg="#2A2A2A", fg="#E0E0E0", font=("Arial", 9, "bold"))
hidden_image_label.grid(row=2, column=1, pady=5)
hidden_image_entry = tk.Entry(input_frame, width=30)
hidden_image_entry.grid(row=3, column=1, pady=5)

# Key phrase input field (spanning both columns)
key_phrase_label = tk.Label(input_frame, text="Enter key phrase:", bg="#2A2A2A", fg="#E0E0E0", font=("Arial", 9, "bold"))
key_phrase_label.grid(row=4, column=0, columnspan=2, pady=5)
key_phrase_text = tk.Text(input_frame, width=50, height=3)
key_phrase_text.grid(row=5, column=0, columnspan=2, pady=10)

# Buttons below the key phrase input field
button1 = tk.Button(input_frame, text="Hide text within image", width=25, command=hidden_txt_within_image, bg="#3D3D3D", fg="#E0E0E0")
button1.grid(row=6, column=0, padx=10, pady=5)

button2 = tk.Button(input_frame, text="Hide image within image", width=25, command=hide_image_within_image, bg="#3D3D3D", fg="#E0E0E0")
button2.grid(row=6, column=1, padx=10, pady=5)

# --- Terminal Output and Image Display ---
# Create a frame for terminal output and image display
output_frame = tk.Frame(tab2, width=600, height=300)
output_frame.pack(pady=10)
output_frame.configure(bg="#2A2A2A")

# Terminal output Text widget
terminal_output = tk.Text(output_frame, wrap="word", height=8, state="disabled", bg="#1E1E1E", fg="#E0E0E0")
terminal_output.pack(padx=10, pady=10, fill="both", expand=True)

# Redirect stdout and stderr to terminal_output
sys.stdout = RedirectOutput(terminal_output)
sys.stderr = RedirectOutput(terminal_output)

# Start the Tkinter event loop
root.mainloop()
