function [] = WordImages_Create_fromPNG(bdir, imFileType, imFolder, sideSize)
%{
bdir       = fullfile(vlRP,'DATA');
imFileType = 'png';
imFolder   = '/Users/glerma/Documents/BCBL_PROJECTS/2022 votc-langorth (Kepa, Manolo)/imagesCHINATEST';
sideSize   = 118; % calculated using the code below


% Calculate the mean size of all other files to create the chines ones
% hh=[];ww=[];for a=1:length(A);tt=imread(A(a).name);hh=[hh,size(tt,1)];ww=[ww,size(tt,2)];end
% meanArea  = mean(ww) * mean(hh);
% sideSize  = round(sqrt(meanArea));
% 
% We control this with samples per point when creeating from text. In PNG
% case we will send the img with the correct size to the renderer


WordImages_Create_fromSVG(bdir, imFileType, imFolder, sidesize)
%}




%% Housekeeping
WordPath     = fullfile(bdir,'output','ZH_PNG');
ImgWritePath = imFolder; % fullfile(bdir, 'images'); 
if ~isfolder(ImgWritePath); mkdir(ImgWritePath); end

% matlabpool ips_base; 

%% Read files
PNGfiles = dir(fullfile(WordPath,'*.png'));

  
% Common variables
SampleImgWritePath = ImgWritePath;
mFont = 'Arial';
mFont_Size = 12;
mSamplesPerPoint = 6;
mPhaseScrambleW = 1;

% Real Words + Phase Scrambled + Scrambled + CB
for ii = 1:length(PNGfiles)
    fname       = fullfile(PNGfiles(ii).folder,PNGfiles(ii).name);
    mPalabraBig = double(rgb2gray(imread(fname)))/256;
    % Resize it
    mPalabra    = imresize(mPalabraBig,sideSize/size(mPalabraBig,1));
    % Compose the correct filename
    [a,b,c] = fileparts(fname);
    d = split(b,'_');
    f = split(d{3},'-');
    if str2num(d{2})<= 80; CB = 'CB1'; else CB = 'CB2'; end
    mImFilename = ['ZH_' CB '_' f{1} c];
    
    if strcmp(d{1},'RW')
        mTipo       = 'all';  
    else
        mTipo       = lower(d{1});  
    end
    RenderWriteWord(mPalabra, mFont, mFont_Size, mSamplesPerPoint, mTipo, ...
                        ImgWritePath, mImFilename, mPhaseScrambleW, imFileType);

end

% matlabpool close;

end



