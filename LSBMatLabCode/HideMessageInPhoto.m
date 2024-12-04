% Load the image
image = imread('loosesprites.png');

% Get height and width for traversing through the image
col = size(image, 1);
row = size(image, 2);

%change img to grey
input=rgb2gray(image);

% Display the image
figure;
imshow(input);
title('converted grey image before hidden bits');

%Secret Message Bits
message=[1 0 1 0];

%message length variable
messageIndex=length(message);

%prepare output
output=input;

%set counter
counter=1;

% Traverse through the image. Image has 3 parts, col, row, and pixel value
% 0-255.
for i = 1 : col
    for j = 1 : row
         
        % check if more bits left in image
        if(counter <= messageIndex)
             
            % Finding the Least Significant Bit of the current pixel since
            % ex: 255 mod 2 gives 1, which is the correct last bit.
            % Basically mod 2 lets you know if the last bit is 1 or 0 or in
            % other words if the numbder is odd or even, you can see if
            % that last bit is a 1 or a 0
            LSB = mod(double(input(i, j)), 2);
             
            % Find whether the bit is same or needs to change
             if LSB ~= message(counter)
                 if message(counter)==1
                     temp=1;
                     % Updating the output to input + temp
                     output(i, j) = input(i, j)+temp;
                 else
                     temp=1;
                     % Updating the output to input + temp
                     output(i, j) = input(i, j)-temp;
                 end
             end

            % Increment the messageIndex
            counter = counter+1;
        end
         
    end
end
imwrite(output,"StegoImage.png")

%create new figure for second image
figure;
imshow("StegoImage.png")
title('grey stego image');
