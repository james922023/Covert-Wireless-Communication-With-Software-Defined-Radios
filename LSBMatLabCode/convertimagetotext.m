% Load the image
image = imread('StegoImage.png');

% Get image dimensions
[height, width] = size(input);

% Open a file to write
fileID = fopen('image_data.txt', 'w');

% Write header information
fprintf(fileID, 'Image dimensions: [%d x %d]\n\n', height, width);
fprintf(fileID, 'Image Data (in the format [row, col, PixelVal]):\n\n');

% Write pixel data
for i = 1:height
    for j = 1:width
        % Get the pixel value
        pixel_value = input(i, j);
        
        % Write formatted data to file
        fprintf(fileID, '[%d, %d, %d]\n', i, j, pixel_value);
    end
end

% Close the file
fclose(fileID);

disp('Image data written to image_data.txt');
