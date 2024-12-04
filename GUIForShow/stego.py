import cv2
import random

def load_image(path):
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError("Image not found.")
    return image

def generate_key_sequence(seed, length):
    random.seed(seed)
    sequence = list(range(length))
    random.shuffle(sequence)
    return sequence

def embed_message(image, message, key):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    msg_len = len(binary_message)
    
    height, width = image.shape
    pixels_count = height * width
    
    key_sequence = generate_key_sequence(key, pixels_count)

    if msg_len > pixels_count:
        raise ValueError("Message is too long for the image size.")
    
    img_copy = image.copy()
    for i in range(msg_len):
        pixel_idx = key_sequence[i]
        x, y = divmod(pixel_idx, width)
        
        img_copy[x, y] = (img_copy[x, y] & 0xFE) | int(binary_message[i])
        
    return img_copy

def extract_message(stego_image, msg_length, key):
    height, width = stego_image.shape
    pixels_count = height * width

    key_sequence = generate_key_sequence(key, pixels_count)
    
    binary_message = ''
    for i in range(msg_length * 8): 
        pixel_idx = key_sequence[i]
        x, y = divmod(pixel_idx, width)
        
        bit = stego_image[x, y] & 1
        binary_message += str(bit)
        
    message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
    return message
