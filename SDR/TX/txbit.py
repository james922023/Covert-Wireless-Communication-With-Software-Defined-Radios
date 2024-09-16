import numpy as np
import adi
import matplotlib.pyplot as plt

sample_rate = 1e6  
sdr = adi.Pluto("ip:192.168.2.1")
sdr.tx_lo = int(2.4e9)
sdr.tx_hardwaregain_chan0 = -10

bits = np.array([1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1])

# ASK modulation
fs = 1e6  # Sampling frequency
fc = 100e3  # Carrier frequency for ASK
bit_rate = 1000  # Bit rate

samples_per_bit = int(fs / bit_rate)
t = np.arange(samples_per_bit) / fs

carrier = np.cos(2 * np.pi * fc * t)

ask_signal = np.hstack([(bit * carrier) for bit in bits])
ask_signal /= np.max(np.abs(ask_signal))
ask_signal_complex = ask_signal + 0j 

sdr.tx(ask_signal_complex)  

plt.plot(np.real(ask_signal[:samples_per_bit*len(bits)])) 
plt.title('ASK Signal ')
plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.show()

sdr.tx_destroy_buffer()