import numpy as np
import adi
import matplotlib.pyplot as plt
import time
from scipy.stats import mode
from PIL import Image

#SET PARAMETERS FOR THE RADIO
sample_rate = 1000000 # Hz
center_freq = 915e6 # Hz
num_samps = 62 # number of samples per call to rx()
ack_freq = 600e6 # Hz

sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)

# Config Tx
sdr.tx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
sdr.tx_lo = int(center_freq)
sdr.tx_hardwaregain_chan0 = -10# Increase to increase tx power, valid range is -90 to 0 dB

# Config Rx
sdr.rx_lo = int(ack_freq)
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = num_samps
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 5 # dB, 0-72

# CREATE TRANSMIT WAVEFORM(BPSK, 2 samples per symbol)
num_symbols = 40
num_wrong_ack_packets = 0
# Define the start sequence
start_sequence = np.array([1,1,1,-1,-1,-1,1,-1,-1,1,-1])
ack_packet = np.array([1,0,1,1,1,0,1,1,1,1])
#CREATE ARRAY OR USE IMAGE ARRAY AS STARTING POINT
x_int = np.random.randint(0,1,1,0,1,0,0,0,0,1,1,0,0,1,0,1,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,1,1)  # 0 to 1 (binary)
print("original bits (1 will be -1 and 0 will be 1): ", x_int)

# Define phase for BPSK: 0 for 0, π for 1
x_radians = x_int * np.pi  # 0 for 0, π for 1
x_symbols = np.cos(x_radians) + 1j * np.sin(x_radians)  # BPSK complex symbols

# Repeat each symbol to create the waveform with 16 samples per symbol
x_symbols = np.repeat(x_symbols, 2)  # 16 samples per symbol

samples = np.concatenate((start_sequence, x_symbols)) # FOR THE GRAPH 0 is positive, 1 is negative

#print("DATA WITH START SEQUENCE: ",bpsk_values)
samples = samples * 2**14  # Scale the samples for PlutoSDR
# Now 'samples' contains the BPSK PACKET to transmit
sdr.tx_cyclic_buffer = True # Enable cyclic buffers
success = False

#sdr.tx(samples) # start transmitting

while not success: #KEEP TRANSMITTING TIL GET ACK PACKET
    #receieve samples
    rx_samples = sdr.rx()
    
    # Cross-correlation of the start sequence with the received signal
    cross_corr = np.correlate(rx_samples, start_sequence, mode='full')

    # Find the index of the peak in the cross-correlation
    peak_index = np.argmax(np.abs(cross_corr))  # Index of the maximum value
    peak_value = cross_corr[peak_index]  # Value of the peak

    #CALCULATE HOW MUCH SAMPLES AFTER THE FOUND INDEX
    samples_after_barker = len(rx_samples)-peak_index
    #HANDLE CASE WITH INCOMPLETE BARKER AT THE END BEING HIGHER CROSS CORRELATION VALUE
    if samples_after_barker < len(ack_packet)-1:
        # If the peak is too close to the end, we need to find the next highest peak
        cross_corr[peak_index] = 0  # Temporarily set the peak to negative infinity
        peak_index = np.argmax(np.abs(cross_corr))  # Find the next peak
        peak_value = cross_corr[peak_index]  # Update peak value
        # Print the results
        #print(f"Updated Peak Value: {peak_value}, Peak Index in Cross-Correlation: {peak_index}")
    else:
        # Print the results
        #print(f" 1st Peak Value: {peak_value}, Peak Index in Cross-Correlation: {peak_index}")
        pass

    # Plot the cross-correlation result
    # Define the lag for plotting the cross-correlation
    # Plot the received samples
    
    extracted_samples = rx_samples[peak_index+1:peak_index+len(ack_packet)+1]
    #print(extracted_samples)
    # Copy the last element and append it to the array
    #extracted_samples = np.append(extracted_samples, extracted_samples[-1])
    #print(extracted_samples)

    # Convert the complex array based on the real part
    if peak_value>0:
        converted_array = np.where(extracted_samples.real > 0, 1, 0)
        #print(converted_array)
    else:
        converted_array = np.where(extracted_samples.real > 0, 0, 1)
        #print(converted_array)

    if np.array_equal(converted_array, ack_packet):
        print('correct ack packet:',converted_array)
        plt.figure(0)
        plt.plot(rx_samples,'.-')
        lag = np.arange(-len(start_sequence) + 1, len(rx_samples))
        # Plot the cross-correlation on the same graph
        # Shift the cross-correlation by the length of the start sequence to align with received signal
        plt.plot(rx_samples, '.', label='Received Signal', alpha=0.5)
        plt.plot(lag + len(start_sequence) - 1, cross_corr, label='Cross-Correlation', color='r')
        plt.title('Received Samples and Cross-Correlation')
        plt.xlabel('Sample Index')
        plt.ylabel('Amplitude / Correlation Value')
        plt.axhline(0, color='grey', lw=0.5, ls='--')  # Add a horizontal line at y=0 for reference
        plt.legend()
        plt.grid()
        print('100% sucess transmission')
        success = True
    else:
        num_wrong_ack_packets +=1
        #exit()
sdr.tx_destroy_buffer()
print("wrong ack packets: ",num_wrong_ack_packets)
plt.show()