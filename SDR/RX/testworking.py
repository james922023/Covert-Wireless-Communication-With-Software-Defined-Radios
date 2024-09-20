import numpy as np
import adi
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, welch
from PIL import Image

# Define parameters
sample_rate = 1e6  # Hz
center_freq = 915e6  # Hz
num_samps = 100000  
bit_rate = 1000  
fc = 100e3  
samples_per_bit = int(sample_rate / bit_rate)
t = np.arange(samples_per_bit) / sample_rate

# Initialize PlutoSDR
sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)
sdr.tx_rf_bandwidth = int(sample_rate)
sdr.tx_lo = int(center_freq)
sdr.tx_hardwaregain_chan0 = -19
sdr.rx_lo = int(center_freq)
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = num_samps
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 33

def image_to_1d_bit_array(image_path):
    # Open the image using PIL
    img = Image.open(image_path)
    # Convert the image to a NumPy array (pixel values)
    img_array = np.array(img)
    # Flatten the 2D or 3D image array to 1D pixel array
    img_1d_array = img_array.flatten()
    # Convert each pixel value to an 8-bit binary representation and concatenate them into one long bit array
    original_bits = np.unpackbits(img_1d_array.astype(np.uint8))
    return original_bits, img_array.shape  # Return the bit array and original shape for later reconstruction 

# Example usage
image_path = "loosesprites.png"  # Replace with your image file path
original_bits, img_shape = image_to_1d_bit_array(image_path)
 
print(f"1D Image Array: {original_bits}")
print(f"Original Image Shape: {img_shape}")

# Define bits for transmission with 10 zeroes at the beginning and end
#original_bits = np.array([1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1,1,1,1,0,1,0,1,0,1,1])  
padding = 10  # Number of zeroes to add
bits = np.concatenate([np.zeros(padding), original_bits])
bits

# ASK modulation
carrier = np.cos(2 * np.pi * fc * t)
ask_signal = np.hstack([(bit * carrier) for bit in bits])
ask_signal /= np.max(np.abs(ask_signal)) 
ask_signal *= 2**12  

# Start the transmitter
sdr.tx_cyclic_buffer = True  
sdr.tx(ask_signal) 

# Receive samples
rx_samples = sdr.rx()

# Stop transmitting and destroy buffer
sdr.tx_destroy_buffer()

# Plot the transmitted ASK signal
plt.figure()
plt.plot(ask_signal[:samples_per_bit * len(bits)])
plt.title('Transmitted ASK Signal')
plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.show()

# Plot received signal in time domain (focusing on the real part)
plt.figure()
plt.plot(np.real(rx_samples[:samples_per_bit * len(bits)]), label="Real Part")
plt.title('Received ASK Signal')
plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.legend()
plt.show()

# Plot frequency spectrum of transmitted and received signals
def plot_spectrum(signal, fs, title):
    if np.iscomplexobj(signal):
        signal = np.abs(signal)  
    f, Pxx = welch(signal, fs, nperseg=1024)
    plt.figure()
    plt.semilogy(f, Pxx)
    plt.title(title)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Power Spectral Density [V**2/Hz]')
    plt.grid()
    plt.show()

plot_spectrum(ask_signal, sample_rate, 'Transmitted ASK Signal Spectrum')
plot_spectrum(rx_samples, sample_rate, 'Received Signal Spectrum')

# Demodulation
def bandpass_filter(signal, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, signal)
    return y

# Filtered signal
filtered_signal = bandpass_filter(np.real(rx_samples), fc - 10e3, fc + 10e3, sample_rate)

# Plot filtered signal
plt.figure()
plt.plot(filtered_signal[:samples_per_bit * len(bits)])
plt.title('Filtered Received Signal')
plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.show()

# Debugging: Visualize average amplitude for each bit segment
average_amplitudes = []
for i in range(len(bits)):
    segment = filtered_signal[i * samples_per_bit:(i + 1) * samples_per_bit]
    avg_amplitude = np.mean(np.abs(segment))
    average_amplitudes.append(avg_amplitude)
    """plt.figure()
    plt.plot(segment)
    plt.title(f'Segment {i + 1} - Avg Amplitude: {avg_amplitude}')
    plt.xlabel('Samples')
    plt.ylabel('Amplitude')
    plt.show()"""

# Detect bits from filtered signal
threshold = 0.5 * np.max(average_amplitudes)

detected_bits = []
for i in range(len(bits)):
    segment = filtered_signal[i * samples_per_bit:(i + 1) * samples_per_bit]
    avg_amplitude = np.mean(np.abs(segment))
    detected_bits.append(1 if avg_amplitude > threshold else 0)

print("Detected Bits:", detected_bits)

# Function to remove 10 zeroes in a row from start and end
def process_bits(detected_bits, padding_length):
    bits = np.array(detected_bits)
    
    # Convert the padding length to a sequence of zeros
    padding_sequence = np.zeros(padding_length, dtype=int)
    
    # Find the index after the padding zeros
    start_index = None
    for i in range(len(bits) - padding_length):
        if np.array_equal(bits[i:i + padding_length], padding_sequence):
            start_index = i + padding_length
            break
    
    if start_index is not None:
        # Extract the elements before the padding sequence
        before_padding = bits[:i]
        # Extract the elements after the padding sequence
        after_padding = bits[start_index:]
        # Concatenate both parts
        processed_bits = np.concatenate([after_padding, before_padding])
    else:
        # No padding found, return the original bits
        processed_bits = bits
    
    return processed_bits

# Process the detected bits
processed_bits = process_bits(detected_bits, padding)
print("Processed Bits:", processed_bits)

