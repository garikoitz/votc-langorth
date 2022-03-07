function kataword = latin2japanese(latword)
%latin2japanase Converts from latin word to katakana word 
%   Just to be used as FF, doesn't need to make any sense
%    I took the code from: 
%    https://sites.psu.edu/symbolcodes/languages/asia/japanese/katakanachart/

% I paired the lating letters randomly to some of the kata chars

latin2kata = {
'a','ア';
'i','イ';
'u','ウ';
'e','エ';
'o','オ';
'b','カ';
'c','キ';
'd','ク';
'f','サ';
'g','ス';
'h','セ';
'j','チ';
'k','ト';
'l','ナ';
'm','ヌ';
'n','ネ';
'p','ハ';
'q','ヒ';
'r','ホ';
's','ラ';
't','リ';
'v','ル';
'w','ロ';
'x','ワ';
'y','ヰ';
'z','ヱ'};

kataword = latword;
for nl=1:length(latword)
    [li,lo]=ismember(latword(nl),latin2kata);
    kataword(nl) = latin2kata{lo,2};
end

end

