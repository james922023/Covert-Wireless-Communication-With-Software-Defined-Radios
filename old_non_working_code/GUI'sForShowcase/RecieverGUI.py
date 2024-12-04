import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess
import os
import sys
import io

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
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        image_label.configure(image=img_tk)
        image_label.image = img_tk

# Create the main window
root = tk.Tk()
root.title("Run Python Scripts")
root.geometry("800x600")

# Frame for buttons and terminal output
left_frame = ttk.Frame(root, width=400, height=600)
left_frame.pack(side="left", fill="y")
left_frame.pack_propagate(False)

# Frame for image display
right_frame = ttk.Frame(root, width=400, height=600)
right_frame.pack(side="right", fill="both", expand=True)
right_frame.pack_propagate(False)

# Add buttons for scripts
buttons_and_scripts = [
    ("1 Radio Image Transmission", "1023L.py"),
    ("2 Radio Text Transmission", "118r.py"),
    ("2 Radio Image Transmission(WIP)", "notDone.py"),
]

for label, script in buttons_and_scripts:
    button = tk.Button(
        left_frame,
        text=label,
        command=lambda script=script: run_script(script),
        width=30,
        height=2
    )
    button.pack(pady=5)

# Terminal output Text widget
terminal_output = tk.Text(left_frame, wrap="word", height=20, state="disabled")
terminal_output.pack(padx=10, pady=10, fill="both", expand=True)

# Redirect stdout and stderr
sys.stdout = RedirectOutput(terminal_output)
sys.stderr = RedirectOutput(terminal_output)

# Image display area
image_label = tk.Label(right_frame, text="No Image Loaded", bg="gray", width=50, height=25)
image_label.pack(pady=20)

# Add a button to load an image
load_image_button = tk.Button(
    right_frame,
    text="Load Image",
    command=display_image,
    width=20,
    height=2
)
load_image_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
