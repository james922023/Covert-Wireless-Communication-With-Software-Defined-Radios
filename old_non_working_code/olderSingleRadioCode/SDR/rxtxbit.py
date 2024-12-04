import numpy as np
import adi
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, welch

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

# Define bits for transmission
bits = np.array([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])  

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
    plt.figure()
    plt.plot(segment)
    plt.title(f'Segment {i + 1} - Avg Amplitude: {avg_amplitude}')
    plt.xlabel('Samples')
    plt.ylabel('Amplitude')
    plt.show()

# Detect bits from filtered signal
threshold = 0.5 * np.max(average_amplitudes)

detected_bits = []
for i in range(len(bits)):
    segment = filtered_signal[i * samples_per_bit:(i + 1) * samples_per_bit]
    avg_amplitude = np.mean(np.abs(segment))
    detected_bits.append(1 if avg_amplitude > threshold else 0)

print("Detected Bits:", detected_bits)
