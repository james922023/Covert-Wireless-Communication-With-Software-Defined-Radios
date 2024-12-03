function simple_gui_with_closable_tabs()
    % Define colors
    bgColor = [30, 30, 30] / 255; % Equivalent to '#1E1E1E'
    fgColor = [224, 224, 224] / 255; % Equivalent to '#E0E0E0'
    btnBgColor = [61, 61, 61] / 255; % Equivalent to '#3D3D3D'

    % Create the main figure
    fig = uifigure('Name', 'Simple GUI', ...
        'Position', [500, 500, 800, 400], ...
        'Color', bgColor); % Set the background color

    % Add a text area to display output
    txtArea = uitextarea(fig, ...
        'Position', [10, 10, 380, 100], ...
        'Editable', 'off', ...
        'BackgroundColor', bgColor, ...
        'FontColor', fgColor, ...
        'HorizontalAlignment', 'left'); % Left-aligned text

    % Add a panel to display figures
    figurePanel = uipanel(fig, ...
        'Title', 'Figure Output', ...
        'Position', [410, 10, 380, 380], ...
        'BackgroundColor', bgColor, ...
        'ForegroundColor', fgColor);

    % Add a tab group to the figure panel
    tabGroup = uitabgroup(figurePanel, ...
        'Position', [10, 50, 360, 300]);

    % Add a button to close all tabs
    closeTabsButton = uibutton(fig, 'push', ...
        'Text', 'Close All Tabs', ...
        'Position', [580, 360, 200, 30], ...
        'BackgroundColor', btnBgColor, ...
        'FontColor', fgColor, ...
        'ButtonPushedFcn', @(btn, event) closeAllTabs(tabGroup));

    % Add Button 1
    btn1 = uibutton(fig, 'push', ...
        'Text', 'Hide Color Image In Color', ...
        'Position', [10, 350, 200, 30], ...
        'BackgroundColor', btnBgColor, ...
        'FontColor', fgColor, ...
        'ButtonPushedFcn', @(btn, event) runProgram1(txtArea, tabGroup));

    % Add Button 2
    btn2 = uibutton(fig, 'push', ...
        'Text', 'Recover Color From Color', ...
        'Position', [10, 300, 200, 30], ...
        'BackgroundColor', btnBgColor, ...
        'FontColor', fgColor, ...
        'ButtonPushedFcn', @(btn, event) runProgram2(txtArea, tabGroup));

    % Add Button 3
    btn3 = uibutton(fig, 'push', ...
        'Text', 'Hide Grey Image in Grey', ...
        'Position', [10, 250, 200, 30], ...
        'BackgroundColor', btnBgColor, ...
        'FontColor', fgColor, ...
        'ButtonPushedFcn', @(btn, event) runProgram3(txtArea, tabGroup));
    % Add Button 4
    btn4 = uibutton(fig, 'push', ...
        'Text', 'Recover Grey Image from Grey', ...
        'Position', [10, 200, 200, 30], ...
        'BackgroundColor', btnBgColor, ...
        'FontColor', fgColor, ...
        'ButtonPushedFcn', @(btn, event) runProgram4(txtArea, tabGroup));
end

% --- Callback for Closing All Tabs ---
function closeAllTabs(tabGroup)
    delete(tabGroup.Children); % Deletes all tabs in the tab group
end

% --- Callback for Button 1 ---
function runProgram1(txtArea, tabGroup)
    txtArea.Value = "Running Program 1...";
    pause(0.5); % Simulate a delay
    try
        addpath('HideColorPhoto'); % Ensure 'HideBitsInGrey' is a valid subfolder

        % Redirect terminal output and capture the script's output
        output = evalc('HideColorPhotoInColorPhoto'); % Ensure 'HideMessageInPhoto.m' exists
        txtArea.Value = output; % Display the script output in the text area

        % Create a new tab for the figure output
        newTab = uitab(tabGroup, 'Title', 'Program 1 Output');
        ax = uiaxes(newTab, 'Position', [10, 10, 330, 300]);

        % Display the output image (replace with your actual image variable)
        img = 'StegoImageC.png'; % Example grayscale image
        imshow(img, 'Parent', ax);
        title(ax, 'Hidden Bits in Grey Image');

        % Add "Close Tab" button
        closeTabButton = uibutton(newTab, 'push', ...
            'Text', 'Close Tab', ...
            'Position', [10, 270, 80, 30], ...
            'ButtonPushedFcn', @(btn, event) delete(newTab));
    catch ME
        txtArea.Value = "Error: " + ME.message; % Display error message
    end
end

% --- Callback for Button 2 ---
function runProgram2(txtArea, tabGroup)
    txtArea.Value = "Running Program 2...";
    pause(0.5); % Simulate a delay
    try
        addpath('HideColorPhotoInColorPhoto'); % Ensure 'HideBitsInGrey' is a valid subfolder
        % Redirect terminal output and capture the script's output
        output = evalc('RecoverColorFromColor'); % Replace 'program2' with your script's name
        txtArea.Value = output; % Display the script output in the text area

        % Create a new tab for the figure output
        newTab = uitab(tabGroup, 'Title', 'Program 2 Output');
        ax = uiaxes(newTab, 'Position', [10, 10, 330, 300]);

        % Display the output image (replace with your actual image variable)
        img = reconstructedImage; % Example grayscale image
        imshow(img, 'Parent', ax);
        title(ax, 'Hidden Black and White Photo');

        % Add "Close Tab" button
        closeTabButton = uibutton(newTab, 'push', ...
            'Text', 'Close Tab', ...
            'Position', [10, 270, 80, 30], ...
            'ButtonPushedFcn', @(btn, event) delete(newTab));
    catch ME
        txtArea.Value = "Error: " + ME.message; % Display error message
    end
end

% --- Callback for Button 3 ---
function runProgram3(txtArea, tabGroup)
    txtArea.Value = "Running Program 3...";
    pause(0.5); % Simulate a delay
    try
        addpath('HideBlackAndWhitePhoto'); % Ensure 'HideBitsInGrey' is a valid subfolder
        % Redirect terminal output and capture the script's output
        output = evalc('HidePhotoinPhoto'); % Replace 'program3' with your script's name
        txtArea.Value = output; % Display the script output in the text area

        % Create a new tab for the figure output
        newTab = uitab(tabGroup, 'Title', 'Program 3 Output');
        ax = uiaxes(newTab, 'Position', [10, 10, 330, 300]);

        % Display the output image (replace with your actual image variable)
        img = 'StegoImage.png'; % Example color image
        imshow(img, 'Parent', ax);
        title(ax, 'Hidden Color Photo');

        % Add "Close Tab" button
        closeTabButton = uibutton(newTab, 'push', ...
            'Text', 'Close Tab', ...
            'Position', [10, 270, 80, 30], ...
            'ButtonPushedFcn', @(btn, event) delete(newTab));
    catch ME
        txtArea.Value = "Error: " + ME.message; % Display error message
    end
end
    % --- Callback for Button 4 ---
function runProgram4(txtArea, tabGroup)
    txtArea.Value = "Running Program 4...";
    pause(0.5); % Simulate a delay
    try
        addpath('HideBitsInGrey'); % Ensure 'HideBitsInGrey' is a valid subfolder
        % Redirect terminal output and capture the script's output
        output = evalc('RecoverPhotofromPhoto'); % Replace 'program3' with your script's name
        txtArea.Value = output; % Display the script output in the text area

        % Create a new tab for the figure output
        newTab = uitab(tabGroup, 'Title', 'Program 4 Output');
        ax = uiaxes(newTab, 'Position', [10, 10, 330, 300]);

        % Display the output image (replace with your actual image variable)
        img = reconstructedImage; % Example color image
        imshow(img, 'Parent', ax);
        title(ax, 'Hidden Color Photo');

        % Add "Close Tab" button
        closeTabButton = uibutton(newTab, 'push', ...
            'Text', 'Close Tab', ...
            'Position', [10, 270, 80, 30], ...
            'ButtonPushedFcn', @(btn, event) delete(newTab));
    catch ME
        txtArea.Value = "Error: " + ME.message; % Display error message
    end
end
