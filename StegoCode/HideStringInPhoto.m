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
[row, col, depth] = size(image);

% Display the image
figure;
imshow(image);
title('original image');

% Prepare output
input = image;
output = input;

% Example input string
message = 'Hello World';

% Preallocate a bit array for the entire string
num_bits = length(message) * 8;  % Each character will be converted to 8 bits
secretMessageArray = []; % Preallocate array

% Convert each character to bits
bit_index = 1;  % Initialize bit index
for i = 1:length(message)
    ascii_value = double(message(i));  % Convert character to ASCII value
    bit_string = dec2bin(ascii_value, 8);  % Convert ASCII to 8-bit binary string
    bits = bit_string - '0';  % Convert binary string to array of numbers (0s and 1s)
    
    % Store the bits in the preallocated array
    secretMessageArray(bit_index:bit_index+7) = bits;
    
    % Update the bit index
    bit_index = bit_index + 8;
end


% Set counter for the bit array
bitIndex = 1;

for i = 1 : row
    for j = 1 : col
        % Embed bits into Red channel
        if bitIndex <= length(secretMessageArray)
            LSB = mod(double(input(i, j, 1)), 2);
            if LSB ~= secretMessageArray(bitIndex)
                if secretMessageArray(bitIndex) == 1
                    output(i, j, 1) = input(i, j, 1) + 1;
                else
                    output(i, j, 1) = input(i, j, 1) - 1;
                end
            end
            bitIndex = bitIndex + 1;
        end
        
        % Embed bits into Green channel
        if bitIndex <= length(secretMessageArray)
            LSB = mod(double(input(i, j, 2)), 2);
            if LSB ~= secretMessageArray(bitIndex)
                if secretMessageArray(bitIndex) == 1
                    output(i, j, 2) = input(i, j, 2) + 1;
                else
                    output(i, j, 2) = input(i, j, 2) - 1;
                end
            end
            bitIndex = bitIndex + 1;
        end
        
        % Embed bits into Blue channel
        if bitIndex <= length(secretMessageArray)
            LSB = mod(double(input(i, j, 3)), 2);
            if LSB ~= secretMessageArray(bitIndex)
                if secretMessageArray(bitIndex) == 1
                    output(i, j, 3) = input(i, j, 3) + 1;
                else
                    output(i, j, 3) = input(i, j, 3) - 1;
                end
            end
            bitIndex = bitIndex + 1;
        end
    end
end

imwrite(output, "StegoImageC.png");

% Create new figure for second image
figure;
imshow("StegoImageC.png");
title('stego image');
disp(secretMessageArray);
disp(length(secretMessageArray));
