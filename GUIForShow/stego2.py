import cv2
import random
import numpy as np

def load_image(path, grayscale=True):
    if grayscale:
        return cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return cv2.imread(path)

def generate_key_sequence(seed, length):
    random.seed(seed)
    sequence = list(range(length))
    random.shuffle(sequence)
    return sequence

def image_to_binary(image):
    binary_image = ''.join(format(pixel, '08b') for row in image for pixel in row)
    return binary_image

def binary_to_image(binary_data, shape):
    pixels = [int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8)]
    return np.array(pixels, dtype=np.uint8).reshape(shape)

def embed_image(host_image, hidden_image, key):
    binary_hidden_image = image_to_binary(hidden_image)
    msg_len = len(binary_hidden_image)
    
    height, width = host_image.shape
    pixels_count = height * width
    
    key_sequence = generate_key_sequence(key, pixels_count)

    if msg_len > pixels_count:
        raise ValueError("Hidden image is too large for the host image.")

    img_copy = host_image.copy()
    for i in range(msg_len):
        pixel_idx = key_sequence[i]
        x, y = divmod(pixel_idx, width)
        img_copy[x, y] = (img_copy[x, y] & 0xFE) | int(binary_hidden_image[i])
        
    return img_copy

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
