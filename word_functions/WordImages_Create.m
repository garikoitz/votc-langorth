function [] = WordImages_Create(WordPath, imFileType)
%{
WordPath = '~/Downloads/VWFA';
imFileType = 'png';

WordImages_Create(WordPath, imFileType)
%}




%% Housekeeping
% clear all; close all; clc;
% WordPath = pwd; % Run it in Stimuli/SoS or Stimuli/ajencia
ImgWritePath = [WordPath, filesep, 'TASKgray']; % GREY60 son solo para Ajencia
if ~isfolder(ImgWritePath); mkdir(ImgWritePath); end
% imFileType = 'png';
% matlabpool ips_base; 

%% Leer archivos que nos interesan
% Ojo con la codificacion, si no es iso8859 no va bien
% arreglar archivos con esto
% iconv -t UTF-8 -f ISO-8859-1 espal_orig.txt > espal_orig_utf8.txt
% Ademas para saber la codificacion usar file -bi filename.txt
cd(WordPath);
if IsLinux
    filesWithRW = dir('RW_*soloword.txt');
    filesWithPW = dir('PW_*soloword.txt');
end
% If you want to take all of them
% Tener esto comentado, leo todas las palabras para crear los task
% filesWithRW = dir('DesdeBASP_UTF8.txt');
% fileID = fopen(fopen(['iso_' filesWithRW(1).name], 'r', 'n', 'ISO-8859-1'));
% [words] = textread(fileID,'%s%*[^\n]', 'headerlines', 1);
% filesWithRW = dir('soloword_ehitz_utf8_ajenciaYlodeSoS_arreglado.txt');
% filesWithRW = dir('nueva_lista_con_60.txt');
% filesWithRW = dir('sinusar_Length456.txt');
% filesWithPW = dir('sinusar_PW_Length456.txt');

%% Clean words from tildes etc. It has to be done in Linux, it doesn't work in Mac.
% Then I save a .mat and open it in mac in order to create the Georgian
% bmp images.

if IsLinux
    RW_group = cell(size(filesWithRW));
    RW_list = cell(size(filesWithRW));
    clean_RW = cell(size(filesWithRW));
    for nfile = 1:length(filesWithRW)
        %system(['iconv -f UTF-8 -t ISO-8859-1 ' filesWithRW(nfile).name ...
        %    ' > iso_' filesWithRW(nfile).name]); 
        % fileID = fopen(fopen(['iso_' filesWithRW(nfile).name], 'r', 'n',...
        %     'ISO-8859-1'));
        fileID = fopen(fopen([filesWithRW(nfile).name], 'r', 'n','utf-8'));
        [words] = textread(fileID,'%s%*[^\n]', 'headerlines', 0);
        cleanwords = words;
        for j = 1:length(cleanwords) 
            	cleanwords{j} = CambiaTilde(cleanwords{j});
        end
        RW_group{nfile} = filesWithRW(nfile).name(4:6);
        RW_list{nfile} = words;
        clean_RW{nfile} = cleanwords;
    end

    save('cleanwords_for_georgian_80t.mat', 'RW_group', 'clean_RW');
end

%% Now we can write the Real Words + Phase Scrambled + Scrambled + CB
if IsLinux
    for nfile = 1:length(RW_group)
        group = RW_group{nfile};
        [words] = RW_list{nfile};
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
    cd(WordPath)
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