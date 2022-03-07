function [ ] = RenderWriteWord(word, fuente, font_size, samples_per_point, tipo, path_to_write, imfilename, PhaseScrambleW, imFileType)
% RenderWriteWord Creates bmp of a word to be used with Presentation
%  Using Vistalabs code, I wanted to do all the coding in Python and just call the required functions
% Example call to this function: 
%       matlab -nodesktop -nojvm -r "RenderWriteWord('perro', 'Courier', 12, 8, 'all', '/export/home/glerma/glerma/BCBLFiles/PROYECTOS/VWFA/Stimuli/SoS/Word_Images', 'perro.bmp');"
% Next version try to do the functions as well in matlab
% fuente can be: - 'Courier' for example
% font_size can be: 12 for example
% samples per point can be: 8 for example
% The checkerboard code has been adapted from vistadisp/makeCheckerboard.m
% Tipo can be: 
%               - 'solo_im': it will write just the word for the behavioral
%               tasks
%               - 'all': it will print the three types, including scrambled
%               and phase scrambled
%               - 'pw': Generate Pseudoword
%               - 'georg': georgiano
%               - 'cs': consontant string
%               - 'cb': chequerboard
%               
    %% Create the original image based on Vistalabs function
    img=my_renderText(word, fuente, font_size, samples_per_point);
    %img=my_renderText('prueba', 'Courier', 12, 8);
    %tipo = 'pw'
    %path_to_write='./'
    %imfilename = 'borrar.png'
    if strcmp(tipo, 'pw')   
        img_filename_with_path = [path_to_write, filesep, 'PW_', imfilename];
    elseif strcmp(tipo, 'georg')
        img_filename_with_path = [path_to_write, filesep, 'FF_', imfilename];    
    elseif strcmp(tipo, 'cs')
        img_filename_with_path = [path_to_write, filesep, 'CS_', imfilename];  
    elseif strcmp(tipo, 'cb')
        img_filename_with_path = [path_to_write, filesep, 'CB_', imfilename];  
    else
        img_filename_with_path = [path_to_write, filesep, 'RW_', imfilename];
    end
    
    %% Trim empty space above and below image
    delrows=[];
    %find top rows with no white in them
    r=1;
    while sum(img(r,:))== 0
        delrows=[delrows, r];
        r=r+1;
    end
    
    %find bottom rows with no white in them
    r=size(img,1);
    while sum(img(r,:))== 0
        delrows=[delrows, r];
        r=r-1;
    end
    
    %remove whiteless rows from top and bottom
    img(delrows,:)=[];
    
    
    %% Create scrambled image
        % ideal tilesize = 10x10
        [height width] = size(img);
        rows= ceil(height/10);
        columns = ceil(width/10);
        
        scb=wordScrambleImage(img, rows, columns);
        scb_filename_with_path = [path_to_write, filesep, 'SD_', imfilename];

        
    %% Create PhaseScrambled image
        pscb=phaseScramble(img, PhaseScrambleW); % w can go from 0 to 1, default 1, amount of phasing it is being done
        pscb_filename_with_path = [path_to_write, filesep, 'PS_', imfilename];

    %% Create checkerboard with same size as word
    
        n = 15; %num pixels per side within a square
        p = 10; %number of rows / 2
        q = 20; %number of columns / 2
        [height width] = size(img);
        
        cropsize = [0, 0, width, height]; 
        
        black = zeros(n);
        % black = 0.5 * ones(n); % Para obtener los cuadrados grises
        white = ones(n);

        % make the 2x2 tiles
        % a ver si consigo randomizarlo
        if rand <= 0.5
            tile = [black white; white black];
            BWcheck = repmat(tile,p,q);
        else
            tile = [white black; black white];
            BWcheck = repmat(tile,p,q);
        end
        
        % crop 
        if ~notDefined('cropsize')
            BWcheck = imcrop(BWcheck,cropsize);
        end

        % display
        % figure(1); imagesc(BWcheck); colormap gray; truesize
        % figure(2); imagesc(BWrevCheck); colormap gray; truesize
        checkerboard_filename_with_path = [path_to_write, filesep, 'CB_', imfilename];
    if strcmp(tipo, 'cb')
        img = BWcheck;
    end
    
    %% Write images according to tipo
    imwrite(img, img_filename_with_path, imFileType); % We do this allways
    if strcmp(tipo, 'all')   
        imwrite(scb, scb_filename_with_path, imFileType);
        imwrite(pscb, pscb_filename_with_path, imFileType);
        imwrite(BWcheck,checkerboard_filename_with_path, imFileType)

    end
end

