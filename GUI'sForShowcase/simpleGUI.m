function simple_gui_with_figures()
    % Create the main figure
    fig = uifigure('Name', 'Simple GUI', 'Position', [500, 500, 800, 400]);

    % Add a text area to display output
    txtArea = uitextarea(fig, ...
        'Position', [10, 10, 380, 100], ...
        'Editable', 'off'); % Make it read-only for output

    % Add a panel to display figures
    figurePanel = uipanel(fig, ...
        'Title', 'Figure Output', ...
        'Position', [410, 10, 380, 380]); % Right side of the GUI

    % Add a tab group to the panel
    tabGroup = uitabgroup(figurePanel, ...
        'Position', [10, 10, 360, 340]);

    % Add Button 1
    btn1 = uibutton(fig, 'push', ...
        'Text', 'Hide Bits In Grey Image', ...
        'Position', [10, 350, 200, 30], ...
        'ButtonPushedFcn', @(btn, event) runProgram1(txtArea, tabGroup));

    % Add Button 2
    btn2 = uibutton(fig, 'push', ...
        'Text', 'Hide Black and White Photo In Image', ...
        'Position', [10, 300, 200, 30], ...
        'ButtonPushedFcn', @(btn, event) runProgram2(txtArea, tabGroup));

    % Add Button 3
    btn3 = uibutton(fig, 'push', ...
        'Text', 'Hide Color Photo In Image', ...
        'Position', [10, 250, 200, 30], ...
        'ButtonPushedFcn', @(btn, event) runProgram3(txtArea, tabGroup));
end

% --- Callback for Button 1 ---
function runProgram1(txtArea, tabGroup)
    txtArea.Value = "Running Program 1...";
    pause(0.5); % Simulate a delay
    try
        % Add the required folder to the MATLAB path
        addpath('HideBitsInGrey'); % Ensure 'HideBitsInGrey' is a valid subfolder

        % Redirect terminal output and capture the script's output
        output = evalc('HideMessageInPhoto'); % Ensure 'HideMessageInPhoto.m' exists
        txtArea.Value = output; % Display the script output in the text area

        % Create a new tab for the figure output
        newTab = uitab(tabGroup, 'Title', 'Program 1 Output');
        ax = uiaxes(newTab, 'Position', [10, 10, 330, 300]);

        % Display the output image (replace with your actual image variable)
        img = 'StegoImage.png'; % Example grayscale image
        imshow(img, 'Parent', ax);
        title(ax, 'Hidden Bits in Grey Image');
    catch ME
        txtArea.Value = "Error: " + ME.message; % Display error message
    end
end

% --- Callback for Button 2 ---
function runProgram2(txtArea, tabGroup)
    txtArea.Value = "Running Program 2...";
    pause(0.5); % Simulate a delay
    try
        % Redirect terminal output and capture the script's output
        output = evalc('program2'); % Replace 'program2' with your script's name
        txtArea.Value = output; % Display the script output in the text area

        % Create a new tab for the figure output
        newTab = uitab(tabGroup, 'Title', 'Program 2 Output');
        ax = uiaxes(newTab, 'Position', [10, 10, 330, 300]);

        % Display the output image (replace with your actual image variable)
        img = rand(256, 256); % Example grayscale image
        imshow(img, 'Parent', ax);
        title(ax, 'Hidden Black and White Photo');
    catch ME
        txtArea.Value = "Error: " + ME.message; % Display error message
    end
end

% --- Callback for Button 3 ---
function runProgram3(txtArea, tabGroup)
    txtArea.Value = "Running Program 3...";
    pause(0.5); % Simulate a delay
    try
        % Redirect terminal output and capture the script's output
        output = evalc('program3'); % Replace 'program3' with your script's name
        txtArea.Value = output; % Display the script output in the text area

        % Create a new tab for the figure output
        newTab = uitab(tabGroup, 'Title', 'Program 3 Output');
        ax = uiaxes(newTab, 'Position', [10, 10, 330, 300]);

        % Display the output image (replace with your actual image variable)
        img = rand(256, 256, 3); % Example color image
        imshow(img, 'Parent', ax);
        title(ax, 'Hidden Color Photo');
    catch ME
        txtArea.Value = "Error: " + ME.message; % Display error message
    end
end
