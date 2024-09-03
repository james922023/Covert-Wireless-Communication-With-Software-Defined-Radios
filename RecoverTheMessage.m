% Load the image
image = imread('StegoImage.png');

% Display the image
%figure;
%imshow(image);

% Get height and width for traversing through the image
col = size(image, 1);
row = size(image, 2);

messageIndex=4;

%set counter
counter=1;

%Store Secret Message Bits
secretMessage=[];

input=image;

% Traverse through the image. Image has 3 parts, col, row, and pixel value
% 0-255.
for i = 1 : col
    for j = 1 : row
        % check if more bits left in image
        if(counter <= messageIndex)
            %grab LSB 
            LSB = mod(double(input(i, j)), 2);
            secretMessage(counter)=LSB;
            % Increment the messageIndex
            counter = counter+1;
        end
         
    end
end
display(secretMessage);

