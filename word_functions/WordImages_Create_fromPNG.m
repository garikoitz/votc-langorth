function [] = WordImages_Create_fromPNG(bdir, imFileType, imFolder, sideSize)
%{
clear all;
bdir       = fullfile(vlRP,'DATA');
imFileType = 'png';
imFolder   = '/Users/glerma/Documents/BCBL_PROJECTS/2022 votc-langorth (Kepa, Manolo)/images';
sideSize   = 138; % calculated using the code below

WordImages_Create_fromPNG(bdir, imFileType, imFolder, sideSize)




% Calculate the mean size of all other files to create the chines ones
%{
    cd('/Users/glerma/Documents/BCBL_PROJECTS/2022 votc-langorth (Kepa, Manolo)/images')
    A = dir('./*.png');
    hh=[];ww=[];for a=1:length(A);tt=imread(A(a).name);hh=[hh,size(tt,1)];ww=[ww,size(tt,2)];end
    meanArea  = mean(ww) * mean(hh);
    sideSize  = round(sqrt(meanArea));
% 
% We control this with samples per point when creeating from text. In PNG
% case we will send the img with the correct size to the renderer
%}

%}


% CREATE FF COPYING THE JAPANESE ONES FROM EN
%{
imFolder = '/Users/glerma/Documents/BCBL_PROJECTS/2022 votc-langorth (Kepa, Manolo)/images';
PNGfiles = dir(fullfile(imFolder,'EN_FF_*.png'));
for pp=1:length(PNGfiles)
    src = PNGfiles(pp).name;
    dsttmp  = strrep(src,'EN','ZH');
    [~,b,c] = fileparts(dsttmp);
    dst = sprintf('%s_%03d%s',b,pp,c);
    copyfile(fullfile(imFolder,src),fullfile(imFolder,dst))
end
%}



% TEST IT
%{
% Select
% n=2;cd('/Users/glerma/Documents/BCBL_PROJECTS/2022 votc-langorth (Kepa, Manolo)/imagesCHINATEST')
% cd(WordPath); n=1;

PNGfiles = dir(fullfile(imFolder,'*.png'));
CB=0;PW=0;CS=0;PS=0;RW=0;SD=0;FF=0;
for ii=1:length(PNGfiles)
    fname = PNGfiles(ii).name; ff = split(fname,'_');
    
    if strcmp(ff{n},'CB');CB=CB+1;end
    if strcmp(ff{n},'PW');PW=PW+1;end
    if strcmp(ff{n},'CS');CS=CS+1;end
    if strcmp(ff{n},'PS');PS=PS+1;end
    if strcmp(ff{n},'RW');RW=RW+1;end
    if strcmp(ff{n},'SD');SD=SD+1;end
    if strcmp(ff{n},'FF');FF=FF+1;end
end
sprintf('CB=%i\nPW=%i\nCS=%i\nPS=%i\nRW=%i\nSD=%i\nFF=%i',CB,PW,CS,PS,RW,SD,FF)


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
    mImFilename = ['ZH_' CB '_' f{1} '_' d{2} c];
    
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



