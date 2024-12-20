import numpy as np
import adi
import matplotlib.pyplot as plt
import time
from scipy.stats import mode
from PIL import Image

#SET PARAMETERS FOR THE RADIO
sample_rate = 1000000 # Hz
center_freq = 915e6 # Hz
num_samps = 12
other_freq = 900e6

sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)

# Config Tx
sdr.tx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
sdr.tx_lo = int(center_freq)
sdr.tx_hardwaregain_chan0 = -10# Increase to increase tx power, valid range is -90 to 0 dB

# Config Rx
sdr.rx_lo = int(other_freq)
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = num_samps
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 0 # dB, 0-72

def int_to_5bit_array(n):
    # Convert to 5-bit binary string and then map each bit to an integer
    binary_str = format(n, '05b')  # Convert integer to 5-bit binary string
    binary_array = np.array([int(bit) for bit in binary_str])  # Convert to a list of integers
    return binary_array

# CREATE TRANSMIT WAVEFORM(BPSK, 2 samples per symbol)
num_symbols = 8192
num_wrong_ack_packets = 0
# Define the start sequence
start_sequence = np.array([1,1,1,-1,-1,-1,1,-1,-1,1,-1])

# CONVERT IMAGE TO ARRAY FOR SENDING
image_path = "C:/Users/dankp/Desktop/EGNSTEGO/TransmissionCodeUpdated/StegoImage.png"
image = Image.open(image_path) #.convert('L')  # Convert to grayscale
# Convert the image to a 2D NumPy array
image_array = np.array(image)
# Initialize an empty list to hold the binary values
binary_image = []
# Manually flatten the 2D array and convert each pixel to binary
height, width = image_array.shape  # Get the dimensions of the image
for row in range(height):
    for col in range(width):
        pixel_value = image_array[row, col]  # Get the pixel value
        # Convert pixel value to an 8-bit binary string
        binary_string = format(pixel_value, '08b')
        # Extend the binary_image list by appending each bit separately
        binary_image.extend([int(bit) for bit in binary_string])
# Convert the list to a NumPy array (if needed)
binary_image = np.array(binary_image)
print('length of binary array', len(binary_image))

# Create arrays and fill them with elements from IMAGE ARRAY
arrays = []
for i in range(16):
    start_index = i * num_symbols  # Start at the correct index for each transmission
    end_index = start_index + num_symbols
    array = binary_image[start_index:end_index]  # Fill array with elements from original_bits
    arrays.append(array)
print("Length of arrays:", len(arrays))

# Initialize an empty list to hold the reconstructed image data
reconstructed_image_bits = []

'''#CREATE ARRAY OR USE IMAGE ARRAY AS STARTING POINT
x_int = np.array([0,1,1,0,1,0,0,0,0,1,1,0,0,1,0,1,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,1,1])  # 0 to 1 (binary)
#print("original bits (1 will be -1 and 0 will be 1): ", x_int)

# Define phase for BPSK: 0 for 0, π for 1
x_radians = x_int * np.pi  # 0 for 0, π for 1
x_symbols = np.cos(x_radians) + 1j * np.sin(x_radians)  # BPSK complex symbols

# Repeat each symbol to create the waveform with 16 samples per symbol
x_symbols = np.repeat(x_symbols, 3)  # 16 samples per symbol'''

for k in range(16):
    ack_packet = int_to_5bit_array(k+1)
    ack_packet = np.where(ack_packet == 0, 1, -1)
    #ack_packet = np.repeat(ack_packet, 3)
    # Define phase for BPSK: 0 for 0, π for 1
    x_radians = arrays[k] * np.pi  # 0 for 0, π for 1
    x_symbols = np.cos(x_radians) + 1j * np.sin(x_radians)  # BPSK complex symbols
    x_symbols = np.repeat(x_symbols, 3)  # 16 samples per symbol
    samples = np.concatenate((start_sequence, ack_packet, x_symbols)) # FOR THE GRAPH 0 is positive, 1 is negative

    #print("DATA WITH START SEQUENCE: ",bpsk_values)
    samples = samples * 2**14  # Scale the samples for PlutoSDR
    # Now 'samples' contains the BPSK PACKET to transmit
    sdr.tx_cyclic_buffer = True # Enable cyclic buffers
    success = False
    
    sdr.tx(samples) # start transmitting
    time.sleep(4)
    '''for i in range(2000):
        sdr.tx(samples) # transmit the batch of samples once'''
    sdr.tx_destroy_buffer()
sdr = None  # Release the SDR object
