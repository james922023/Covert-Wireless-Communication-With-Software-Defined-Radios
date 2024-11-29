import numpy as np
import adi
import matplotlib.pyplot as plt
import time
from scipy.stats import mode
from PIL import Image
import tkinter
import matplotlib

matplotlib.use('TkAgg')

#SET PARAMETERS FOR THE RADIO
sample_rate = 1e6 # Hz
center_freq = 915e6 # Hz
num_samps = 100000 # number of samples per call to rx()

#SETUP THE TRANSMITTER IP
sdr = adi.Pluto("ip:192.168.2.1")

#SETUP THE RECIEVER IP
#sdr2 = adi.Pluto("ip:192.168.3.1")

#SET THE SAMPLE RATE FOR THE TRANSMITTER
sdr.sample_rate = int(sample_rate)

#SET THE SAMPLE RATE FOR THE RECEIVER
#sdr2.sample_rate = int(sample_rate)

# Config Tx BANDWIDTH, FREQUENCY, and GAIN
sdr.tx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
sdr.tx_lo = int(center_freq)
sdr.gain_control_mode_chan0 = 'manual'
sdr.tx_hardwaregain_chan0 = -10# Increase to increase tx power, valid range is -90 to 0 dB

# Config Rx Bandwidth, Frequency, buffersize, and gain
#sdr2.rx_rf_bandwidth = int(sample_rate)
#sdr2.rx_lo = int(center_freq)
#sdr2.rx_buffer_size = num_samps
#sdr2.gain_control_mode_chan0 = 'manual'
#sdr2.rx_hardwaregain_chan0 = 0 # dB, 0-72

#CREATE A 11 LENGTH BARKER SEQUENCE TO USE FOR CROSS CORRELATION
start_sequence = np.array([1,1,1,-1,-1,-1,1,-1,-1,1,-1])

#SET VARIABLES FOR NUMBER OF SYMBOLS IN A PACKET
num_symbols = 100

#SET VARIABLE TO GET HOW MUCH EACH SYMBOL IS REPEATED
sps = 3

#CREATE THE SIGNAL OF THE SYMBOLS
x_int = np.random.randint(0,2,num_symbols)
x_radians = x_int * np.pi
x_symbols = np.cos(x_radians)
x_symbols = np.repeat(x_symbols,3)

#PRINT THE MAX AND MIN VALUES OF THE SIGNAL TO MAKE SURE IT WILL FIT WITHIN THE RANGE ALLOWED TO BE TRANSMITTED
print(np.min(x_symbols),np.max(x_symbols))

#ADD THE BARKER SEQUENCE TO THE FRONT OF THE SIGNAL
samples = np.concatenate((start_sequence,x_symbols))

#PRINT OUT THE LENGTH OF THE SAMPLES TO SHOW HOW MANY AFTER REPETITION AND BARKER
print(len(samples))

#MULTIPLY BE 2^14 FOR PLUTO
samples = samples * 2**14

#TRANSMIT THE SAMPLES
sdr.tx_cyclic_buffer = False 
sdr.tx(samples)
#time.sleep(.01)

#RECEIVE THE SAMPLES
#for i in range(5):
#    rx_samples = sdr2.rx()
#    plt.figure(i+1)
#    plt.plot(rx_samples.real,'.-')

#DESTROY BUFFER AFTER THE TRANSMISSION
sdr.tx_destroy_buffer()

#REMOVE OBJECT
sdr=None

#FOR VISUALIZATION PRINT ORIGINAL BITS ALONG WITH PLOTTING THE SIGNAL
print(x_int)

plt.figure(0)
plt.plot(samples.real,'.-')


plt.show()


