import numpy as np
import adi
import matplotlib.pyplot as plt
import time
from scipy.stats import mode
from PIL import Image

# CONVERT IMAGE TO ARRAY FOR SENDING
image_path = 'StegoImage.png'  # Replace with your image path
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

#SET PARAMETERS FOR THE RADIO
sample_rate = 1000000 # Hz
center_freq = 915e6 # Hz
num_samps = 150000 # number of samples per call to rx()

sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)

# Config Tx
sdr.tx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
sdr.tx_lo = int(center_freq)
sdr.tx_hardwaregain_chan0 = -19# Increase to increase tx power, valid range is -90 to 0 dB

# Config Rx
sdr.rx_lo = int(center_freq)
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = num_samps
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 33 # dB, 0-72

# CREATE TRANSMIT WAVEFORM(BPSK, 2 samples per symbol)
num_symbols = 8192
# Define number of samples per symbol
samples_per_symbol = 4  # Change to 2 or 4 as needed
lengthofData = num_symbols*samples_per_symbol
# Define the start sequence
start_sequence = np.array([1,1,1,-1,-1,1,-1])
#REPEAT IT TO BE 10% size of PACKET SIZE
start_sequence = np.tile(start_sequence, 1170)

#CREATE ARRAY OR USE IMAGE ARRAY AS STARTING POINT
#x_int = np.random.randint(0, 2, num_symbols)  # 0 to 1 (binary)
#print("original data: ", x_int)

# Calculate number of transmissions
larger_size = len(binary_image)
num_transmissions = int(larger_size / num_symbols)
print("Number of transmissions:", num_transmissions)

# Create arrays and fill them with elements from original_bits
arrays = []
for i in range(num_transmissions):
    start_index = i * num_symbols  # Start at the correct index for each transmission
    end_index = start_index + num_symbols
    array = binary_image[start_index:end_index]  # Fill array with elements from original_bits
    arrays.append(array)
print("Length of arrays:", len(arrays))

# Initialize an empty list to hold the reconstructed image data
reconstructed_image_bits = []

# Transmission loop
for transmission_index in range(num_transmissions):
    # Convert PACKET to BPSK values: 0 -> -1, 1 -> +1 AND ADD BARKERSEQQUENCE TO PRODUCE PACKET SIGNAL
    bpsk_values = arrays[transmission_index] * 2 - 1  # Multiply by 2 and subtract 1
    #print("BPSK OF DATA: ",bpsk_values)
    #REPEAT EVERY SYMBOL variable NUMBER OF TIMES
    # Oversample BPSK values
    bpsk_values_oversampled = np.repeat(bpsk_values, samples_per_symbol)
    #print("repeated sample signal: ",bpsk_values_oversampled)
    # ADD BARKER SEQUENCE TO BPSK
    bpsk_values = np.concatenate((start_sequence, bpsk_values_oversampled))
    #print("DATA WITH START SEQUENCE: ",bpsk_values)
    samples = bpsk_values * 2**14  # Scale the samples for PlutoSDR
    # Now 'samples' contains the BPSK PACKET to transmit
    retries = 0
    success = False
    sdr.tx_destroy_buffer()
    sdr.rx_destroy_buffer()
    sdr.tx_cyclic_buffer = True # Enable cyclic buffers
    sdr.rx_cyclic_buffer = True
    sdr.tx(samples) # start transmitting
    while not success:
        #receieve samples
        rx_samples = sdr.rx()

        #print("transmitted samples: ",samples)
        # Stop transmitting
        sdr.tx_destroy_buffer()
        sdr.rx_destroy_buffer()
        #print("received samples: ",np.real(rx_samples))

        # Process the received samples to convert to binary
        binary_samples = np.where(np.real(rx_samples) > 0, 1, -1)

        # Print the processed binary samples
        #print("Received samples (binary):", binary_samples)


        #FIND THE INDEX OF THE BUFFER WHERE THE START OF FILE STARTS
        seq_length = len(start_sequence)
        print("length of stat seqquence",len(start_sequence))
        start_index = None

        # Outer loop through binary_samples
        for i in range(len(binary_samples)):
            match = True
            
            # Inner loop to check for sequence match
            for j in range(seq_length):
                if i + j >= len(binary_samples) or binary_samples[i + j] != start_sequence[j]:
                    match = False
                    break
            
            # If a match is found, save the index
            if match:
                start_index = i
                break
        print(start_index)
        
        if start_index==None:
            retries=retries+1
            if(retries<4):
                print(f"retry# {retries}")
                #clear buffer
                sdr.tx(samples) # start transmitting
                continue
            else:
                print("gave up, transmission failed 4 times")
                #print("received samples from failed transmission",rx_samples)
                error_array=np.ones(num_symbols)
                print("Filled erorr transmission with 1's: ",error_array)
                reconstructed_image_bits.extend(error_array)
                break
            
        """# Check for START INDICATOR AFTER THE FOUND ONE
        for k in range(start_index + (num_symbols * samples_per_symbol), len(binary_samples)):
            match = True
    
            # Inner loop to check for sequence match
            for l in range(seq_length):
                if k + l >= len(binary_samples) or binary_samples[k + l] != start_sequence[l]:
                    match = False
                    break
    
            # If a match is found, save the index
            if match:
                print("found another start sequence after the current message")
                start_index = k  # Update to the start of the new sequence
                print(start_index)
                break
        """
        # TAKE OUT THE DATA FROM THE BUFFER STARTING FROM INDEX FOUND
        if start_index is not None:
            end_index = start_index + lengthofData + seq_length
            # Slice the array
            sliced_values = binary_samples[start_index:end_index]
        else:
            sliced_values = None  # Handle case where start_index is None

        #print("sliced values: ",sliced_values)
        
        #PROCESS THE SLICED VALUES FINDING THE MODE THIS WILL GIVE BPSK THAT SHOULD MATCH INPUT ONE EXCLUDING THE STARTING SEQUENCE

        # Initialize the result array
        x_int_received = []
        # Skip the first 7 elements
        sliced_values = sliced_values[seq_length:]
        # Process the array in chunks of 4
        for m in range(0, len(sliced_values), samples_per_symbol):
            chunk = sliced_values[m:m+samples_per_symbol]
            if len(chunk) < samples_per_symbol:  # Skip incomplete chunks
                break
            mean_value = np.mean(chunk)
            if mean_value > 0:
                x_int_received.append(1)
            else:
                x_int_received.append(0)

        # Output the result
        #print("x_int_received:", x_int_received)
        # Check for equality using an if statement
        if np.array_equal(x_int_received, arrays[transmission_index]):
            # Add x_int_received to reconstructed_image_bits
            reconstructed_image_bits.extend(x_int_received)
            print("100% Sucess in transmission")
            success = True
            
        else:
            print("Bits arent 100%")
            reconstructed_image_bits.extend(x_int_received)
            break
#After all transmissions, concatenate the reconstructed image bits and reshape to the original image dimensions
reconstructed_image_bits = np.array(reconstructed_image_bits, dtype=np.uint8)
reconstructed_image = np.packbits(reconstructed_image_bits).reshape(image.size)
# Convert the NumPy array back to an image
reconstructed_image = Image.fromarray(reconstructed_image, mode='L')
# Save the image to a file
reconstructed_image.save('transmittedimage.png')