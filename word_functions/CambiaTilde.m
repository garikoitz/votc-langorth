function [cleaned] = CambiaTilde(word)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
    chars_old = 'ÁÉÍÓÚáéíóúÑñÜü';
    chars_new = 'AEIOUaeiouNnUu';
    [tf, loc] = ismember(word, chars_old);
    word(tf) = chars_new(loc(tf));
    cleaned = word;
end

