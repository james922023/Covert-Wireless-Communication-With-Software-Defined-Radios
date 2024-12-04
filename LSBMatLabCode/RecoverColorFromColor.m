% Load the image
image = imread('StegoImageC.png');

%show THE STEGO IMAGE
figure;
imshow('StegoImageC.png')
title('stego image');

% Secret Image Dimensions and number of bits Hardcoded, but placed in header
% of image later
rows = 128;
cols = 128;
depth= 3;

% Get height and width for traversing through the image
col = size(image, 1);
row = size(image, 2);

% Set counter
counter = 1;

%size of each channel
numbitsInImg2 = 131072;

% Store Secret Message Bits
% Initialize bit arrays for each color channel
LSB_R = zeros(numbitsInImg2, 1);
LSB_G = zeros(numbitsInImg2, 1);
LSB_B = zeros(numbitsInImg2, 1);

input = image;

bitIndex = 1;
% Traverse through the image and extract LSBs
for i = 1:row
    for j = 1:col
        if bitIndex <= numbitsInImg2
            % Extract LSB from Red channel
            LSB_R(bitIndex) = mod(double(image(i, j, 1)), 2);
            
            % Extract LSB from Green channel
            LSB_G(bitIndex) = mod(double(image(i, j, 2)), 2);
            
            % Extract LSB from Blue channel
            LSB_B(bitIndex) = mod(double(image(i, j, 3)), 2);
            
            bitIndex = bitIndex + 1;
        end
    end
end

% Display the number of elements in the secretMessage array
totalBitsinarrays = length(LSB_R) + length(LSB_G) + length(LSB_B);
disp(['Number of bits in secretMessage arrays: ', num2str(totalBitsinarrays)]);

% Reconstruct the image
reconstructedImage = zeros(rows, cols, 3, 'uint8');

% Reconstruct Red channel
bitIndex = 1;
for i = 1:rows
    for j = 1:cols
        pixelValue = 0;
        for b = 1:8
            bit = LSB_R(bitIndex);
            pixelValue = bitset(pixelValue, 9 - b, bit);
            bitIndex = bitIndex + 1;
        end
        reconstructedImage(i, j, 1) = pixelValue;
    end
end

% Reconstruct Green channel
bitIndex = 1;
for i = 1:rows
    for j = 1:cols
        pixelValue = 0;
        for b = 1:8
            bit = LSB_G(bitIndex);
            pixelValue = bitset(pixelValue, 9 - b, bit);
            bitIndex = bitIndex + 1;
        end
        reconstructedImage(i, j, 2) = pixelValue;
    end
end

% Reconstruct Blue channel
bitIndex = 1;
for i = 1:rows
    for j = 1:cols
        pixelValue = 0;
        for b = 1:8
            bit = LSB_B(bitIndex);
            pixelValue = bitset(pixelValue, 9 - b, bit);
            bitIndex = bitIndex + 1;
        end
        reconstructedImage(i, j, 3) = pixelValue;
    end
end

% Display the reconstructed image
figure;
imshow(reconstructedImage);
title('Reconstructed Image');

