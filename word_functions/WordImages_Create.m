function [] = WordImages_Create(bdir, imFileType, imFolder)
%{
bdir = fullfile(vlRP,'DATA');
imFileType = 'png';
imFolder   = '/Users/glerma/Documents/BCBL_PROJECTS/2022 votc-langorth (Kepa, Manolo)/images';

WordImages_Create(WordPath, imFileType)
%}




%% Housekeeping
% clear all; close all; clc;
% WordPath = pwd; % Run it in Stimuli/SoS or Stimuli/ajencia
WordPath     = fullfile(bdir,'output');
ImgWritePath = imFolder; % fullfile(bdir, 'images'); 
if ~isfolder(ImgWritePath); mkdir(ImgWritePath); end

% matlabpool ips_base; 

%% Read RW and PW files and generate the table
filesWithRW = dir(fullfile(WordPath,'RW_*justwords.txt'));
filesWithPW = dir(fullfile(WordPath,'PW_*justwords.txt'));

WS       = table();
N        = 80;
   
for nfile =1:length(filesWithRW)
    fileID      = fopen(fopen(fullfile(WordPath,filesWithRW(nfile).name), 'r', 'n','utf-8'));
    [words]     = textread(fileID,'%s%*[^\n]', 'headerlines', 0);
    tmpt        = table();
    tmpt.WORD   = categorical(words);
    tmpt.LANG   = categorical(repmat({filesWithRW(nfile).name(4:5)},[N,1]));
    tmpt.TYPE   = categorical(repmat({filesWithRW(nfile).name(1:2)},[N,1]));
    tmpt.CB     = categorical(repmat({filesWithRW(nfile).name(7:9)},[N,1]));
    tmpt.cWORD  = categorical(cellfun(@CambiaTilde, words,'UniformOutput', false));
    tmpt.wname  = categorical(strcat(char(tmpt.LANG(1)),'_',...
                                    char(tmpt.TYPE(1)),'_',...
                                    char(tmpt.CB(1)),'_',...
                                    cellstr(tmpt.cWORD),...
                                    '.',imFileType));
    % PW
    tmpt.PW     = categorical(readtable(fullfile(WordPath,filesWithPW(nfile).name)).Match); 
    tmpt.pwname = categorical(strrep(cellstr(tmpt.wname),'RW','PW'));
    tmpt.name   = categorical(strrep(cellstr(tmpt.wname),'RW_',''));
    % CS
    tmpt.CS     = categorical(cellfun(@pw2cs, cellstr(tmpt.PW),'UniformOutput', false));
    % FF
    if strcmp(filesWithRW(nfile).name(4:5),'ZH')
        tmpt.FF     = tmpt.CS;
    else
        tmpt.FF     = categorical(cellfun(@latin2japanese, cellstr(tmpt.cWORD),'UniformOutput', false));
    end
    
    % Concatenate with the rest of the files
    WS = [WS;tmpt];
end

%% Now we can write the images 
% Common variables
SampleImgWritePath = ImgWritePath;
mFont = 'Arial';
mFont_Size = 12;
mSamplesPerPoint = 6;
mPhaseScrambleW = 1;

% Real Words + Phase Scrambled + Scrambled + CB
parfor ii = 1:height(WS)
    mPalabra    = char(WS.WORD(ii));
    mImFilename = char(WS.name(ii));
    mTipo       = 'all';  
    RenderWriteWord(mPalabra, mFont, mFont_Size, mSamplesPerPoint, mTipo, ...
                        ImgWritePath, mImFilename, mPhaseScrambleW, imFileType);
% end

% PW image generation
% parfor ii = 1:height(WS)
    mPalabra    = char(WS.PW(ii));
    % mImFilename = char(WS.name(ii));
    mTipo       = 'pw';  
    RenderWriteWord(mPalabra, mFont, mFont_Size, mSamplesPerPoint, mTipo, ...
                        ImgWritePath, mImFilename, mPhaseScrambleW, imFileType);
% end

% CS image generation
% parfor ii = 1:height(WS)
    mPalabra    = char(WS.CS(ii));
    % mImFilename = char(WS.name(ii));
    mTipo       = 'cs';  
    RenderWriteWord(mPalabra, mFont, mFont_Size, mSamplesPerPoint, mTipo, ...
                        ImgWritePath, mImFilename, mPhaseScrambleW, imFileType);
% end

% FF image generation
% parfor ii = 1:height(WS)
    mPalabra    = char(WS.FF(ii));
    % mImFilename = char(WS.name(ii));
    mTipo       = 'ff';  
    RenderWriteWord(mPalabra, mFont, mFont_Size, mSamplesPerPoint, mTipo, ...
                        ImgWritePath, mImFilename, mPhaseScrambleW, imFileType);
end

% matlabpool close;

end