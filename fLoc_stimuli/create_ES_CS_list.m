% this script is used to create cs from the pw list
% I beg there is one thing that is here for doing that, 

wordlist_dir='/Users/tiger/toolboxes/votc-langorth/DATA/output';
pwlist1=readtable(fullfile(wordlist_dir, "PW_ES_CB1_80_justwords.txt"));
pwlist2=readtable(fullfile(wordlist_dir, "PW_ES_CB2_80_justwords.txt"));

cslist1=pwlist1;
cslist2=pwlist2;

for i = 1:height(cslist1)
    cslist1.Match(i) = {pw2cs(cslist1.Match{i})};
end


for i = 1:height(cslist2)
    cslist1.Match(i) = {pw2cs(cslist2.Match{i})};
end


writecell(pwlist1.Match, fullfile(wordlist_dir, "PW_ES_CB1_80_pwonly.txt"));
writecell(pwlist2.Match, fullfile(wordlist_dir, "PW_ES_CB2_80_pwonly.txt"));
writecell(cslist1.Match, fullfile(wordlist_dir, "CS_ES_CB1_80_csonly.txt"));
writecell(cslist2.Match, fullfile(wordlist_dir, "CS_ES_CB2_80_csonly.txt"));