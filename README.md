# GOALS OF THIS PROJECT
1. Hide data in an image using Least Significant Bit Steganography that is to be sent between software defined radios

2. Hide the Signal being sent between software defined radios leveraging DSSS to spread the signal making it noiselike.

Combining these two will allow the wireless communication to be covert.

# WHAT IS CURRENTLY WORKING IN THIS REPO

Right now, we have a transmission system for a PlutoSDR that allows the Pluto to send an image to itself using its full duplex capabilities. We were also able to have a short DSSS spreading sequence applied to this, and it still transmitted and received perfectly fine. As for two radios, we were only able to reliably send a short message like hello once, and sixteen times, between two PlutoSDR's on seperate computers. In addition to the transmission, we have matlab code that fully works and implements LSB steganography. This code can work on matlabonline, and was implemented there.

#HOW TO USE WHAT HAS BEEN MADE HERE, TO TEST AND POTENTIALLY IMPROVE
1. Once you have a computer and a PlutoSDR, you should follow the instructions on this website https://pysdr.org/ . More specifically this section:

![image](https://github.com/user-attachments/assets/801ab391-ec2b-4bcb-83fc-353dfd64d965)

Its recommended to use linux in a VM as it was pretty straightforward to setup. You can also setup the pluto to work on windows, but you would need to go through extra steps, and look into that.

One thing to help with this process is that in the INSTALLING PLUTOSDR DRIVER section, when I set it up, there was not all of the dependancies installed just by copy and pasting into the terminal. To help make things go more smoothly ill help you out and recommend geting a virtual environment and installing everything you need in there. Once you have a virtual environment, you can activate that, and then run pip list to see what you have and what dependancies you still need. Below I will put a screenshot of everything I had installed:

![image](https://github.com/user-attachments/assets/664d873b-4244-4345-910f-cf65f99c915d)

![image](https://github.com/user-attachments/assets/ee0209bb-df3e-4101-b6c9-d210bce20d73)

*Note, this is my anaconda prompt, because I ended up also getting the pluto Running on my windows computer, but its the same thing if I pip list on ubunutu.


Once your environment is setup, you should be able run the transmitting and receiving simultaneously code from https://pysdr.org/content/pluto.html#transmitting-and-receiving-simultaneously and your figure should be roughly the same.

![image](https://github.com/user-attachments/assets/f36cc663-208c-4176-9e16-6214c6be0bb0)

Once you confirm this runs, you should be able to run any of the python files in the project. For any matlab ones, you would need to use matlab online or download matlab to run those.
