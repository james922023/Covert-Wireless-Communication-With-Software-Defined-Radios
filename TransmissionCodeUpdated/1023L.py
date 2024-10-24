import numpy as np
import adi
import matplotlib.pyplot as plt
import time
from scipy.stats import mode
from PIL import Image

#SET PARAMETERS FOR THE RADIO
sample_rate = 1000000 # Hz
center_freq = 915e6 # Hz
num_samps = 32812 # number of samples per call to rx()

sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)

# Config Tx
sdr.tx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
sdr.tx_lo = int(center_freq)
sdr.tx_hardwaregain_chan0 = -10# Increase to increase tx power, valid range is -90 to 0 dB

# Config Rx
sdr.rx_lo = int(center_freq)
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = num_samps
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 0 # dB, 0-72

# CREATE TRANSMIT WAVEFORM(BPSK, 2 samples per symbol)
num_symbols = 8192
# Define the start sequence
start_sequence = np.array([1,1,1,-1,-1,-1,1,-1,-1,1,-1])










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
print('length of binary array', len(binary_image))


# Calculate number of transmissions
larger_size = len(binary_image)
num_transmissions = int(larger_size / num_symbols)
print("Number of transmissions:", num_transmissions)

# Create arrays and fill them with elements from IMAGE ARRAY
arrays = []
for i in range(num_transmissions):
    start_index = i * num_symbols  # Start at the correct index for each transmission
    end_index = start_index + num_symbols
    array = binary_image[start_index:end_index]  # Fill array with elements from original_bits
    arrays.append(array)
print("Length of arrays:", len(arrays))

# Initialize an empty list to hold the reconstructed image data
reconstructed_image_bits = []










total_suc=0
total_fail=0




sdr.tx_cyclic_buffer = False # Enable cyclic buffers
sdr.rx_cyclic_buffer = False
# Transmission loop
for transmission_index in range(num_transmissions):
    
    #CREATE ARRAY OR USE IMAGE ARRAY AS STARTING POINT
    x_int = arrays[transmission_index]
    
    # Define phase for BPSK: 0 for 0, π for 1
    x_radians = x_int * np.pi  # 0 for 0, π for 1
    x_symbols = np.cos(x_radians) + 1j * np.sin(x_radians)  # BPSK complex symbols
    
    # Repeat each symbol to create the waveform with 16 samples per symbol
    x_symbols = np.repeat(x_symbols, 2)  # 16 samples per symbol
    
    samples = np.concatenate((start_sequence, x_symbols)) # FOR THE GRAPH 0 is positive, 1 is negative
    success = False
    #print("DATA WITH START SEQUENCE: ",bpsk_values)
    samples = samples * 2**14  # Scale the samples for PlutoSDR
    # Now 'samples' contains the BPSK PACKET to transmit
    
    #sdr.tx(samples) # start transmitting
    
    for i in range(4):
        sdr.tx(samples) # transmit the batch of samples once
    

    max_attempts = 5
    sleep_time = 1  # Start with 0.01 second delay
    attempts = 0
    
    while not success:
        #receieve samples
        rx_samples = sdr.rx()
        #print("transmitted samples: ",samples)
        
        plt.figure(0)
        plt.plot(rx_samples,'.-')
        
        # Cross-correlation of the start sequence with the received signal
        cross_corr = np.correlate(rx_samples, start_sequence, mode='full')
        
        # Find the index of the peak in the cross-correlation
        peak_index = np.argmax(np.abs(cross_corr))  # Index of the maximum value
        peak_value = cross_corr[peak_index]  # Value of the peak
        
        #CALCULATE HOW MUCH SAMPLES AFTER THE FOUND INDEX
        samples_after_barker = len(rx_samples)-peak_index
        #HANDLE CASE WITH INCOMPLETE BARKER AT THE END BEING HIGHER CROSS CORRELATION VALUE
        if samples_after_barker < (num_symbols*2)-1:
            # If the peak is too close to the end, we need to find the next highest peak
            cross_corr[peak_index] = 0  # Temporarily set the peak to negative infinity
            peak_index = np.argmax(np.abs(cross_corr))  # Find the next peak
            peak_value = cross_corr[peak_index]  # Update peak value
            # Print the results
            print(f"Updated Peak Value: {peak_value}, Peak Index in Cross-Correlation: {peak_index}")
        else:
            # Print the results
            print(f" 1st Peak Value: {peak_value}, Peak Index in Cross-Correlation: {peak_index}")
        
        # Plot the cross-correlation result
        # Define the lag for plotting the cross-correlation
        lag = np.arange(-len(start_sequence) + 1, len(rx_samples))
        # Plot the received samples
        plt.plot(rx_samples, '.', label='Received Signal', alpha=0.5)
        
        # Plot the cross-correlation on the same graph
        # Shift the cross-correlation by the length of the start sequence to align with received signal
        plt.plot(lag + len(start_sequence) - 1, cross_corr, label='Cross-Correlation', color='r')
        
        plt.title('Received Samples and Cross-Correlation')
        plt.xlabel('Sample Index')
        plt.ylabel('Amplitude / Correlation Value')
        plt.axhline(0, color='grey', lw=0.5, ls='--')  # Add a horizontal line at y=0 for reference
        plt.legend()
        plt.grid()
        #plt.show()
        extracted_samples = rx_samples[peak_index+1:peak_index+num_symbols*2]
        print(extracted_samples)
        # Copy the last element and append it to the array
        extracted_samples = np.append(extracted_samples, extracted_samples[-1])
        #print(extracted_samples)
        
        # Convert the complex array based on the real part
        if peak_value>0:
            converted_array = np.where(extracted_samples.real > 0, 0, 1)
            #print(converted_array)
        else:
            converted_array = np.where(extracted_samples.real > 0, 1, 0)
            #print(converted_array)
            
        # Remove redundancy (take every second element)
        reduced_array = converted_array[::2]
        #print("Converted Array without Redundancy:", reduced_array)
        if attempts < 4 :
            if np.array_equal(reduced_array, x_int):
                print('100% sucess transmission')
                total_suc+=1
                success = True
                # Stop transmitting
                sdr.tx_destroy_buffer()
                sdr.rx_destroy_buffer()
                # Concatenate reduced_array to reconstructed_image_bits
                reconstructed_image_bits.extend(reduced_array)
            else:
                print(f'Transmission not 100% (Attempt {attempts + 1})')
                time.sleep(sleep_time)  # Sleep for the increasing delay
                sleep_time += 1  # Increment the sleep time by 0.01 second
                attempts += 1  # Increase the attempt count
                plt.figure(6)
                plt.plot(extracted_samples,'.-')
                plt.show()
                exit()
        else:
            print('giving up')
            total_fail+=1
            # Stop transmitting
            sdr.tx_destroy_buffer()
            sdr.rx_destroy_buffer()
            break
            
        #plt.show()
print(total_suc)
print(total_fail)
#After all transmissions, concatenate the reconstructed image bits and reshape to the original image dimensions
reconstructed_image_bits = np.array(reconstructed_image_bits, dtype=np.uint8)
reconstructed_image = np.packbits(reconstructed_image_bits).reshape(image.size)
# Convert the NumPy array back to an image
reconstructed_image = Image.fromarray(reconstructed_image, mode='L')
# Save the image to a file
reconstructed_image.save('transmittedimage.png')




