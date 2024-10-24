# This is where we will store our project code as we develop it.
# The Stegocode so far...(9/2/2024)
-HideMessageInPhoto as of now hides a bit sequence 1010 inside the image after the image is converted to black and white. Its converted to black and white for simplicity.

-RecoverTheMessage as of now takes the black and white image and has hardcoded preknowledge of message size. It loops through the image and then extracts the bits, putting it into an array and then spits out the hidden bit sequence into the console.

# The Stegocode as of (9/06/2024)

-We are able to embed a bit sequence and decode it from a black and white image and then extract it

-We are able to embed a smaller black and white photo in a larger one and then extract it

-We are able to embed a smaller colored image inside a larger one amd then extract it

-We are able to embed a string or sentence inside a colored image then extract it

# TRANSMISSION CODE as of 10/24/2024

-working transmission and reception on one radio(full duplex).
  -break down an image into bits
  -break down image into 8192 or 1kb sized arrays
  -creates a BPSK signal with 2 symbols per bit of that image array.
  -Each transmission has a 11 length barker sequence as the preamble
  -transmits these signals over in a loop
    -each time a signal is received, receiver looks for premable with cross correlation and then takes out the 2*1kb worth of sin numbers from the samples
    -from here, the extracted bits are then processed removing redundancy and converting back to 0 and 1
    -these 0's and 1's are placed in back into an array, that once all loops are finsihed, should have the reconstructed image information
  -reconstructs the image back to png and saves it to computer from the image array that was appended to after each loop
  
-has a short 4 length DSSS spreading sequence version that also works, just has a spreading step before transmission that is applied only to the data and not the preabmle, and also a despreading step that is done after the preamble is found and the spreaded bits are extracted.
