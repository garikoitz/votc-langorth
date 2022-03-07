bdir  = fullfile(vlRP,'DATA','output');
% words = dir(fullfile(bdir,'RW_*F*Length456_80.txt'));
words = dir(fullfile(bdir,'RW_*'));
warning('off','all')
fprintf('INFO: RW = Real Words, N = 80 (2 groups), Word Length : 4-5-6\n')
% fprintf('      LF = Low Frequency, HF = High Frequency\n')
frequs = nan(80,length(words));
for ii=1:length(words)
    thislist = readtable(fullfile(bdir,words(ii).name),'HeaderLines', 0,'ReadRowNames',false);
    fprintf('Mean frequency (std dev) for %s is: %g (%g)\n', ...
      strrep(words(ii).name,'_80.txt',''),mean(thislist.fre_f),std(thislist.fre_f))
  % Add freq col for anova
  frequs(:,ii) = thislist.fre_f;
end
% Perform ANOVA to see if all those freq means are the same or not across all
% languages
fprintf('ANOVA between the frequ of all files to check they have same frequ: \n')
anova1(frequs)


ls     = nan(80,length(words));
for ii=1:length(words)
    thislist = readtable(fullfile(bdir,words(ii).name),'HeaderLines', 0,'ReadRowNames',false);
    fprintf('Mean length (std dev) for %s is: %g (%g)\n', ...
      strrep(words(ii).name,'_80.txt',''),mean(thislist.l_f),std(thislist.l_f))
  % Add freq col for anova
  ls(:,ii)     = thislist.l_f;
end
fprintf('ANOVA between the length of all files to check they have same frequ: \n')
anova1(ls)