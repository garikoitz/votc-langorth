function [] = WordImages_Create(bdir, imFileType)
%{
bdir = fullfile(vlRP,'DATA');
imFileType = 'png';

WordImages_Create(WordPath, imFileType)
%}




%% Housekeeping
% clear all; close all; clc;
% WordPath = pwd; % Run it in Stimuli/SoS or Stimuli/ajencia
WordPath     = fullfile(bdir,'output');
ImgWritePath = fullfile(bdir, 'images'); 
if ~isfolder(ImgWritePath); mkdir(ImgWritePath); end

% matlabpool ips_base; 

%% Read only word files
filesWithRW = dir(fullfile(WordPath,'RW_*justwords.txt'));
filesWithPW = dir(fullfile(WordPath,'PW_*justwords.txt'));

RW       = table();
colnames = {'LANG','TYPE','CB','WORD','cWORD'};
N        = 80;
   
for nfile = 1:length(filesWithRW)
    fileID     = fopen(fopen(fullfile(WordPath,filesWithRW(nfile).name), 'r', 'n','utf-8'));
    [words]    = textread(fileID,'%s%*[^\n]', 'headerlines', 0);
    tmpt       = table();
    tmpt.WORD  = categorical(words);
    tmpt.LANG  = categorical(repmat({filesWithRW(nfile).name(4:5)},[N,1]));
    tmpt.TYPE  = categorical(repmat({filesWithRW(nfile).name(1:2)},[N,1]));
    tmpt.CB    = categorical(repmat({filesWithRW(nfile).name(7:9)},[N,1]));
    tmpt.cWORD = categorical(cellfun(@CambiaTilde, words,'UniformOutput', false));
    
    % Concatenate with the rest of the files
    RW = [RW;tmpt];
end

PW       = table();
colnames = {'LANG','TYPE','CB','WORD','cWORD'};
N        = 80;
   
for nfile = 1:length(filesWithPW)
    fileID     = readtable(fullfile(WordPath,filesWithPW(nfile).name));
    [words]    = fileID.Match;
    tmpt       = table();
    tmpt.WORD  = categorical(words);
    tmpt.LANG  = categorical(repmat({filesWithRW(nfile).name(4:5)},[N,1]));
    tmpt.TYPE  = categorical(repmat({filesWithRW(nfile).name(1:2)},[N,1]));
    tmpt.CB    = categorical(repmat({filesWithRW(nfile).name(7:9)},[N,1]));
    tmpt.cWORD = categorical(cellfun(@CambiaTilde, words,'UniformOutput', false));
    
    % Concatenate with the rest of the files
    PW = [PW;tmpt];
end

%% Now we can write the Real Words + Phase Scrambled + Scrambled + CB
for nfile = 1:length(RW_group)
    group        = RW_group{nfile};
    [words]      = RW_list{nfile};
    [cleanwords] = clean_RW{nfile};
    
    WordFilenames = strcat(group, '_', cleanwords, '.', imFileType);
    
    parfor i = 1:length(words)
        mPalabra = char(words(i));
        mImFilename = char(WordFilenames(i));
        mFont = 'Arial';
        mFont_Size = 12;
        mSamplesPerPoint = 8;
        mPhaseScrambleW = 1;
        mTipo = 'all';  % 'all' o 'solo_im'
        SampleImgWritePath = ImgWritePath;
        % LLamada a la funcion
        RenderWriteWord(mPalabra, mFont, mFont_Size, mSamplesPerPoint, mTipo, ImgWritePath, mImFilename, mPhaseScrambleW, imFileType);
    end
end


%% Here we generate the pseudoword images
if IsLinux
    PW_list = cell(size(filesWithPW));
    PW_group = cell(size(filesWithPW));
    clean_PW = cell(size(filesWithPW));
    for nfile = 1:length(filesWithPW)
        % system(['iconv -f UTF-8 -t ISO-8859-1 ' filesWithPW(nfile).name ' > iso_' filesWithPW(nfile).name]); 
        % pfileID = fopen(fopen(['iso_' filesWithPW(nfile).name], 'r', 'n', 'ISO-8859-1'));
        pfileID = fopen(fopen([filesWithPW(nfile).name], 'r', 'n', 'UTF-8'));
        PW_group{nfile} = filesWithPW(nfile).name(4:6);
        
       
        if isequal(PW_group{nfile},RW_group{nfile})
            clean_PW{nfile} = clean_RW{nfile};
        else
            error('Diferent indexing in RW and PW');
        end
        
        [pwords] = textread(pfileID,'%*s%s%*[^\n]', 'headerlines', 1);
        size(pwords)
        WordFilenames = strcat(PW_group{nfile}, '_', clean_PW{nfile}, '.', imFileType);

        parfor i = 1:length(pwords)
            mPalabra = char(pwords(i));
            mImFilename = char(WordFilenames(i));
            mFont = 'Arial';
            mFont_Size = 12;    
            mSamplesPerPoint = 8;
            mPhaseScrambleW = 1;
            mTipo = 'pw';
            SampleImgWritePath = ImgWritePath;
            % LLamada a la funcion
            RenderWriteWord(mPalabra, mFont, mFont_Size, mSamplesPerPoint, mTipo, ImgWritePath, mImFilename, mPhaseScrambleW, imFileType);
        end
    end
end

%% And now the consontant strings
if IsLinux
    PW_list = cell(size(filesWithPW));
    PW_group = cell(size(filesWithPW));
    clean_PW = cell(size(filesWithPW));
    CS_list = cell(size(filesWithPW));
    for nfile = 1:length(filesWithPW)
        % system(['iconv -f UTF-8 -t ISO-8859-1 ' filesWithPW(nfile).name ' > iso_' filesWithPW(nfile).name]); 
        pfileID = fopen(fopen([filesWithPW(nfile).name], 'r', 'n', 'ISO-8859-1'));
        PW_group{nfile} = filesWithPW(nfile).name(4:6);
        
        if isequal(PW_group{nfile},RW_group{nfile})
            clean_PW{nfile} = clean_RW{nfile};
        else
            error('Diferent indexing in RW and PW');
        end
        
        [cswords] = textread(pfileID,'%*s%s%*[^\n]', 'headerlines', 1);
        
        WordFilenames = strcat(PW_group{nfile}, '_', clean_PW{nfile}, '.', imFileType);

        parfor i = 1:length(cswords)
            word = cswords{i};
            chars_old = 'aeiou';
            consonants = 'bcdfghjklmnpqrstvwxyz';
            chars_new = datasample(consonants, 5);
            [tf, loc] = ismember(word, chars_old);
            word(tf) = chars_new(loc(tf));
            mPalabra = char(word);
            mFont = 'Arial';
            mFont_Size = 12;
            mSamplesPerPoint = 8;
            mPhaseScrambleW = 1;
            mTipo = 'cs';
            SampleImgWritePath = ImgWritePath;
            mImFilename = char(WordFilenames(i));
            % LLamada a la funcion
            RenderWriteWord(mPalabra, mFont, mFont_Size, mSamplesPerPoint, mTipo, ImgWritePath, mImFilename, mPhaseScrambleW, imFileType);
        end
    end
end


%% OJO: ONLY TO BE EXECUTED IN MAC AFTER THE PREVIOUS ONE HAS BEEN EXECUTED IN LINUX
% We read the word_list and continue from here

% Update comments above, here I will try to read the words in UTF with tildes
% and everything and then remove the tildes before converting them to japanese
% characters
if ismac

    W = readtable('RW_HF2Length456_80.txt', 'VariableNamingRule','preserve');
    W.Properties.VariableNames = strrep(W.Properties.VariableNames,'|','_');
    % Clean words from tildes
    cleanwords = cellfun(@CambiaTilde, W.word_s,'UniformOutput', false);
    
    % Find and substitute by the corresponding Japanese Katakana character
    % I took the code from: https://sites.psu.edu/symbolcodes/languages/asia/japanese/katakanachart/
    
    for nfile = 1:length(xxxxxgroups here)
        [cleanwords] = clean_RW{nfile};
        group = RW_group{nfile};

        WordFilenames = strcat('FF', '_', cleanwords, '.', imFileType);
        mPalabras     = cellfun(@latin2japanese, cleanwords, 'UniformOutput', false);
        
        
        parfor ii = 1:length(mPalabras)
            ii
            mPalabra = mPalabras{ii};
            mFont = 'Arial';
            mFont_Size = 12;
            mSamplesPerPoint = 8;
            mPhaseScrambleW = 1;
            mTipo = 'georg';
            SampleImgWritePath = ImgWritePath;
            mImFilename = char(WordFilenames(ii));
            % LLamada a la funcion
            RenderWriteWord(mPalabra, mFont, mFont_Size, mSamplesPerPoint, ...
                 mTipo, ImgWritePath, mImFilename, mPhaseScrambleW, imFileType);
        end
    end
end

%% Execute manually: create phase scrambled version of faces
% faces = dir('FC*');
% for nfile=1:length(faces)
%     myPhaseScramble(faces(nfile).name, ['PF_',faces(nfile).name]);
% end
% 
matlabpool close;
% si hay problemas poner matlabpool force close;
end