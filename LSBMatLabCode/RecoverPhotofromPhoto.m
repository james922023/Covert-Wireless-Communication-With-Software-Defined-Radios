% Load the image
image = imread('StegoImage.png');

%show THE STEGO IMAGE
figure;
imshow('StegoImage.png')
title('stego image');

% Read in the original grayscale image
originalImage = imread('loosesprites.png');
originalImageGrey = rgb2gray(originalImage);

%DEBUGGING

% Display the first few pixel values of the original grayscale image
%disp('First few pixel values of the original grayscale image:');
%disp(originalImageGrey(1:3));

% Secret Image Dimensions and number of bits Hardcoded, but placed in header
% of image later
rows = 128;
cols = 128;

% num bits signaled by EOF character later rendition
numbitsInImg2 = 131072;

% Get height and width for traversing through the image
col = size(image, 1);
row = size(image, 2);

messageIndex = numbitsInImg2;

% Set counter
counter = 1;

% Store Secret Message Bits
secretMessage = [];

input = image;

% Traverse through the image. Image has 3 parts, col, row, and pixel value
% 0-255.
for i = 1 : col
    for j = 1 : row
        % Check if more bits left in image
        if(counter <= messageIndex)
            % Grab LSB 
            LSB = mod(double(input(i, j)), 2);
            secretMessage(counter) = LSB;
            % Increment the messageIndex
            counter = counter + 1;
        end
    end
end
%display first 24 bits of secret message to see if they match
disp(secretMessage(1:32));
% Display the number of elements in the secretMessage array
disp(['Number of bits in secretMessage array: ', num2str(length(secretMessage))]);

%reconstruct the iamge
reconstructedImage=zeros(rows,cols,'uint8');

bitIndex=1;

for i=1:rows
    for j=1:cols
        pixelValue=0;
        for b=1:8
            bit=secretMessage(bitIndex);
            pixelValue=bitset(pixelValue,9-b,bit);
            bitIndex=bitIndex+1;
        end
        reconstructedImage(i,j)=pixelValue;
    end
end

% Display the reconstructed image
figure;
imshow(reconstructedImage, []);
title('Reconstructed Image');

% Debugging: Display the first 10 pixel values of the reconstructed image

%disp('First 10 pixel values of the reconstructed image:');
%disp(reconstructedImage(1:10));

