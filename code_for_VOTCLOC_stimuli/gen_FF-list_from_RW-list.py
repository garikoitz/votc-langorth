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

input_output_file = {f"{code}_RW_80.txt": f"{code}_FF_80.txt" for code in lang}

# Define the English-to-Georgian mapping
latin_to_geo = {
    'a': 'ა', 'e': 'ე', 'i': 'ი', 'o': 'ო', 'u': 'უ',  # Vowels
    'b': 'ბ', 'd': 'დ', 'f': 'ფ', 'g': 'გ', 'h': 'ჰ',
    'j': 'ჯ', 'k': 'კ', 'l': 'ლ', 'm': 'მ', 'n': 'ნ',
    'p': 'პ', 'q': 'ქ', 'r': 'რ', 's': 'ს', 't': 'ტ',
    'w': 'წ', 'x': 'ხ', 'z': 'ზ',  # Consonants

    # German special characters
    'ä': 'ა̈', 'ö': 'ო̈', 'ü': 'უ̈', 'ß': 'სს',

    # French accented vowels
    'é': 'ე́', 'è': 'ე̀', 'ê': 'ე̂', 'ë': 'ე̈',
    'à': 'ა̀', 'â': 'ა̂', 
    'ù': 'უ̀', 'û': 'უ̂',
    'î': 'ი̂', 'ï': 'ი̈',
    'ô': 'ო̂', 

    # French special consonant
    'ç': 'ც'
}


for ip in input_output_file.keys():
    ip_word_listn = open(join(word_dir, ip),'r').readlines()
 
    # iterating to check vowels in string
    op_word_listn = ip_word_listn.copy()
    for i,w in enumerate(op_word_listn):
        tmp_word = ip_word_listn[i]
        for latin, geo in latin_to_geo.items():
            # replacing vowel with the specified character
            tmp_word = tmp_word.replace(latin, geo)
        op_word_listn[i] = tmp_word

    with open(join(word_dir, input_output_file[ip]), mode='w') as f:
        f.write("".join(str(w) for w in op_word_listn))
        