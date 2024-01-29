import os
import random
from PIL import Image, ImageDraw, ImageFont

join = os.path.join



# FOLDERS
homedir = os.getenv('HOME')
word_dir = join(homedir,'toolboxes/votc-langorth/DATA/output')
backgrounds_directory = join(homedir,"soft/fLoc/stimuli/scrambled")
base_output_dir = join(homedir,"soft/SHINEtoolbox/SHINE_INPUT/")


input_output_file = {
    'RW_EU_CB1_80_justwords.txt':'CS_EU_CB1_80_justwords.txt',
    'RW_EU_CB2_80_justwords.txt':'CS_EU_CB2_80_justwords.txt',
}


for ip in input_output_file.keys():
    ip_word_listn = open(join(word_dir, ip),'r').readlines()
    # string of vowels
    vowels = 'aeiou'
    # consonants = 'bcdfghjklmnpqrstvwxyz'
    consonants_EU = 'bdfghjklmnpqrstwxz'
 
    # iterating to check vowels in string
    op_word_listn = ip_word_listn.copy()
    for i,w in enumerate(op_word_listn):
        tmp_word = ip_word_listn[i]
        for ele in vowels:
            # replacing vowel with the specified character
            tmp_word = tmp_word.replace(ele, random.choice(consonants_EU))
        op_word_listn[i] = tmp_word

    with open(join(word_dir, input_output_file[ip]), mode='w') as f:
        f.write("".join(str(w) for w in op_word_listn))
        