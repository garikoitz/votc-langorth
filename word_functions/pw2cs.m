function cs = pw2cs(pw)
% (pseudo)word to consonant string
  

chars_old  = 'aeiou';
consonants = 'bcdfghjklmnpqrstvwxyz';
chars_new  = datasample(consonants, 5);
[tf, loc]  = ismember(pw, chars_old);
pw(tf)     = chars_new(loc(tf));
cs         = pw;


end

