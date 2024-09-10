% Load the image
image = imread('StegoImageC.png');

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
numbitsInImg2 = 88;


secretMessageArray = []; % Preallocate array

input = image;

bitIndex = 1;
% Traverse through the image and extract LSBs
for i = 1:row
    for j = 1:col
        if bitIndex <= numbitsInImg2
            % Extract LSB from Red channel
            secretMessageArray(bitIndex) = mod(double(input(i, j, 1)), 2);
            bitIndex = bitIndex + 1;
        end
        if bitIndex <= numbitsInImg2
            % Extract LSB from Green channel
            secretMessageArray(bitIndex) = mod(double(input(i, j, 2)), 2);
            bitIndex = bitIndex + 1;
        end
        if bitIndex <= numbitsInImg2
            % Extract LSB from Blue channel
            secretMessageArray(bitIndex) = mod(double(input(i, j, 3)), 2);
            bitIndex = bitIndex + 1;
        end
        
    end
end

%SHOW SECRET MESSAGE ARRAY
%%disp(length(secretMessageArray));

% Initialize an empty string to store the decoded message
message = '';

% Loop through the bit array in chunks of 8 bits
for i = 1:8:length(bit_array)
    % Extract 8 bits
    bits = bit_array(i:i+7);
    
    % Convert bits to a binary string
    bit_string = num2str(bits);
    bit_string = bit_string(~isspace(bit_string));  % Remove spaces
    
    % Convert binary string to decimal (ASCII value)
    ascii_value = bin2dec(bit_string);
    
    % Convert ASCII value to character and append to message
    message = [message, char(ascii_value)];
end

% Display the decoded message
disp(['Decoded message: ', message])


