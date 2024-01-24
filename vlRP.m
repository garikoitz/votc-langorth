function rootPath = vlRP()
% Determine path to root of the mrVista directory
%
%        rootPath = vistaRootPath;
%
% This function MUST reside in the directory at the base of the
% MINI directory structure 
%
% Copyright Stanford team, mrVista, 2018

rootPath = which('vlRP');

rootPath = fileparts(rootPath);

return
    