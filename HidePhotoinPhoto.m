% Load the image
image = imread('SpiderManMeme.png');

% Show size of image
filelocation = 'SpiderManMeme.png';
mytemp = filelocation;
fileInfo = dir(mytemp);
disp("number of bytes in the host image: " + fileInfo.bytes);
numBytes = fileInfo.bytes;

% Calculate what size color image and black and white can fit inside this image
largestBlackAndWhiteImage = sqrt(numBytes / 8);
largestColorImage = sqrt((numBytes / 8) / 3);
disp("largest Black and White Image that can fit in host: " + largestBlackAndWhiteImage + "x" + largestBlackAndWhiteImage);
disp("Largest Color Image that can fit in host: " + largestColorImage + "x" + largestColorImage);

% Get height and width for traversing through the image
col = size(image, 1);
row = size(image, 2);

% Change img to grey
input = rgb2gray(image);

% Display the image
figure;
imshow(input);
title('grey original image');

% Secret Message Bits
message = [1 0 1 0];

% Message length variable
messageIndex = length(message);

% Prepare output
output = input;

% Set counter
counter = 1;

% Read in image to hide inside other image
image2 = imread('loosesprites.png');
image2grey = rgb2gray(image2);

% Get rows and columns for smaller image
[rows, cols] = size(image2grey);

% Index for bitArray
bitArrayIndex = 1;

% Show size of image
numBitsInGreyImage = rows * cols * 8;
disp("num bits in grey image: " + numBitsInGreyImage);

%DEBUGGING

%%disp("rows in grey image: " + rows);
%disp("cols in grey image: " + cols);
%disp(image2grey(1:3));


% Initialize a logical array to store bits
bitArray = zeros(numBitsInGreyImage, 1);

% Index for bitArray
bitIndex = 1;

% Loop through the grey image and store bits in array
for i = 1 : cols
    for j = 1 : rows
        % Get pixel value
        pixelValue = image2grey(i, j);
        
        % Extract each bit from pixelValue
        for b = 1:8
            bit = bitget(pixelValue, 9 - b);
            bitArray(bitIndex) = bit;
            bitIndex = bitIndex + 1;
        end
    end
end

% Debugging: Display the first 32 pixel values before embedding

%disp('First 24 bit values before embedding:');
%disp(bitArray(1:32));

for i = 1 : col
    for j = 1 : row
        % Check if more bits left in image
        if(counter <= numBitsInGreyImage)
            % Finding the Least Significant Bit of the current pixel
            LSB = mod(double(input(i, j)), 2);
             
            % Find whether the bit is same or needs to change
            if LSB ~= bitArray(counter)
                if bitArray(counter) == 1
                    temp = 1;
                    % Updating the output to input + temp
                    output(i, j) = input(i, j) + temp;
                else
                    temp = 1;
                    % Updating the output to input + temp
                    output(i, j) = input(i, j) - temp;
                end
            end

            % Increment the messageIndex
            counter = counter + 1;
        end
    end
end



imwrite(output, "StegoImage.png");

% Create new figure for second image
figure;
imshow("StegoImage.png");
title('grey stego image');
