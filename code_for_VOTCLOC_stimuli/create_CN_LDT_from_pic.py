import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
join = os.path.join
import re
import shutil
'''
This script will simply read the output in the DATA/CN_material/derivatives

it will create 2 sub directory; CB1 and CB2

'''
homedir = os.getenv('HOME')
# if in linux, need to add one tlei
base_output_dir =join(homedir,'Desktop') # join(homedir,"soft",'Behav_LDT')
# VARIABLES
langs=['CN'] #['AT','EN','ES','EU','FR','IT']
cats=['RW','CS','PW']

source_dir=os.path.join(homedir, 'toolboxes/votc-langorth/DATA/CN_material/derivatives/beh')

def clean_CN_filenames(source_dir, lang, cat, base_output_dir):
    '''
    This function will according to the src_file_dir to get a list of files,

    Then it will rename it based on the pattern

    Then it will cp the src dir to the targ dir with the new name

    also it will seperate them into 2 groups: group1: CN_CS_#.png group2 CN_CN2_#.png

    '''
    src_file_dir=os.path.join(source_dir,  f'{lang}_{cat}')
    os.makedirs(base_output_dir, exist_ok=True)
    cb1_dir = os.path.join(base_output_dir, 'CTB_I',lang)
    cb2_dir = os.path.join(base_output_dir, 'CTB_II',lang)
    os.makedirs(cb1_dir, exist_ok=True)
    os.makedirs(cb2_dir, exist_ok=True)

    src_png_list = [f for f in os.listdir(src_file_dir) if f.endswith('.png')]

    for fname in src_png_list:
        src_path = os.path.join(src_file_dir, fname)

        # Match CS_###_NAME_crop.png
        match = re.match(rf'{re.escape(cat)}_(\d+)_.*\.png', fname)
        if match:
            num = int(match.group(1))
            new_cs_name = f'{lang}_{cat}_{num}.png'

            if num < 81:
                new_name = f'{lang}_{cat}_{num}.png'
                dst_path = os.path.join(cb1_dir, new_name)
            else:
                new_num = num - 80
                new_name = f'{lang}_{cat}2_{new_num}.png'
                dst_path = os.path.join(cb2_dir, new_name)

            shutil.copy(src_path, dst_path)
            print(f"{fname} → {new_name}")

    return

for lang in langs:
    for cat in cats:
        clean_CN_filenames(source_dir, lang, cat, base_output_dir)