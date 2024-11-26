import os
import random
from PIL import Image, ImageDraw, ImageFont

join = os.path.join

# FOLDERS
homedir = os.getenv('HOME')
# for the linux machine, add tlei before toolbox
word_dir = join(homedir,'tlei','toolboxes/votc-langorth/DATA/wordlist_for_VOTCLOC')
backgrounds_directory = join(homedir,'tlei',"soft/fLoc/stimuli/scrambled")

lang=['AT','EN','ES','EU','FR','IT']

input_output_file = {f"{code}_RW_80.txt": f"{code}_CS_80.txt" for code in lang}

for ip in input_output_file.keys():
    ip_word_listn = open(join(word_dir, ip),'r').readlines()
    # string of vowels
    if ip.split('_')[0]=='IT':
        vowels = 'aeiouàèéìòù'
        consonants = 'bcdfghjklmnpqrstvz'
    elif ip.split('_')[0]=='EN':
        vowels = 'aeiou'
        consonants = 'bcdfghjklmnpqrstvwxyz'
    elif ip.split('_')[0]=='AT':
        vowels = 'aeiouäöü'
        consonants = 'bcdfghjklmnpqrßstvwxyz'      
    elif ip.split('_')[0]=='FR':
        vowels = 'aeiouéèêëàâùûîïô'
        consonants = 'bcdfghjklmnpqrçstvwxyz'  
    elif ip.split('_')[0]=='ES':
        vowels = 'aeiouáéíóúü'
        consonants = 'bcdfghjklmnñpqrstvwxyz'
    elif ip.split('_')[0]=='EU':
        vowels = 'aeiouáéíóú'
        consonants = 'bcdfghjklmnñprstvwxyz'       
    # iterating to check vowels in string
    op_word_listn = ip_word_listn.copy()
    for i,w in enumerate(op_word_listn):
        tmp_word = ip_word_listn[i]
        for ele in vowels:
            # replacing vowel with the specified character
            tmp_word = tmp_word.replace(ele, random.choice(consonants))
        op_word_listn[i] = tmp_word

    with open(join(word_dir, input_output_file[ip]), mode='w') as f:
        f.write("".join(str(w) for w in op_word_listn))
