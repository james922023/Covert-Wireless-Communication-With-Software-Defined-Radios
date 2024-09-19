import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.signal import butter, filtfilt

# Define parameters
sample_rate = 1e6  # Hz
center_freq = 915e6  # Hz
bit_rate = 1000  # Bits per second
fc = 100e3  # Carrier frequency for ASK
samples_per_bit = int(sample_rate / bit_rate)
t = np.arange(samples_per_bit) / sample_rate

# --- Read Image and Convert to Bits ---
img = Image.open("loosesprites.png").convert('L')  # L mode = grayscale
img_array = np.array(img)

# Flatten the image array and convert each pixel value to binary (8 bits per pixel)
img_bits = np.unpackbits(img_array.flatten())

# Define the total number of bits to transmit
num_bits = len(img_bits)

# ASK modulation
carrier = np.cos(2 * np.pi * fc * t)
ask_signal = np.hstack([(bit * carrier).astype(np.float32) for bit in img_bits])
ask_signal /= np.max(np.abs(ask_signal))  # Normalize
ask_signal *= 2**12  # Scale for a realistic signal amplitude

# Simulate channel noise
noise_power = 0.01 * np.max(ask_signal)
rx_samples = ask_signal + np.random.normal(0, np.sqrt(noise_power), len(ask_signal))

# --- Demodulation ---

def bandpass_filter(signal, lowcut, highcut, fs, order=5):
    """ Bandpass filter to isolate the signal around the carrier frequency. """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, signal)

# Filter the received signal to extract the transmitted bits
filtered_signal = bandpass_filter(np.real(rx_samples), fc - 10e3, fc + 10e3, sample_rate)

# Debugging: Visualize average amplitude for each bit segment
average_amplitudes = []
for i in range(num_bits):
    segment = filtered_signal[i * samples_per_bit:(i + 1) * samples_per_bit]
    avg_amplitude = np.mean(np.abs(segment))
    average_amplitudes.append(avg_amplitude)

# Print some average amplitudes for debugging
print("First 100 average amplitudes: ", average_amplitudes[:100])

# Detect bits from filtered signal
# Adjust the threshold dynamically based on the distribution of amplitudes
threshold = 0.5 * (np.max(average_amplitudes) + np.min(average_amplitudes))

detected_bits = []
for i in range(num_bits):
    segment = filtered_signal[i * samples_per_bit:(i + 1) * samples_per_bit]
    avg_amplitude = np.mean(np.abs(segment))
    detected_bits.append(1 if avg_amplitude > threshold else 0)

# Print detected bits (first 100) to check if they are accurate
print("First 100 detected bits: ", detected_bits[:100])
print("Detected Bits Length:", len(detected_bits))

# --- Reconstruct Image from Detected Bits ---

# Convert the list of detected bits back into bytes
detected_bits_array = np.array(detected_bits, dtype=np.uint8)

# Ensure detected bits length matches the original image bits length
if len(detected_bits_array) != len(img_bits):
    print(f"Error: Mismatch in bit lengths. Original: {len(img_bits)}, Detected: {len(detected_bits_array)}")

# Pack bits into bytes
received_bytes = np.packbits(detected_bits_array)

# Reshape the bytes back into the original image dimensions
try:
    received_img_array = received_bytes.reshape(img_array.shape)
except ValueError as e:
    print(f"Error during reshaping: {e}. Ensure the detected bits are correctly packed.")

# Convert the received image array into an image and save it
received_img = Image.fromarray(received_img_array)

# Save the reconstructed image
received_img.save("reconstructed_image.png")
print("Reconstructed image saved as 'reconstructed_image.png'")
