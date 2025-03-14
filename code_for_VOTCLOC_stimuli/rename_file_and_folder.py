import os
import fnmatch
import shutil
# for the fLoc 

homedir = os.getenv('HOME')
# if in linux, need to add one tlei
base_dir = os.path.join(homedir, "toolboxes/fLoc/stimuli")

langs=['CN'] #['AT','EN','ES','EU','FR','IT']
cats=['RW','CS','FF','SC']
CB_group=1
orig_targ_dict = {f"{code}_{cat}": f"{code}_{cat}{CB_group}" for code in langs for cat in cats }

def rename_folder_and_files(base_dir, orig_name, targ_name):
    orig_folder=os.path.join(base_dir,orig_name)
    targ_folder=os.path.join(base_dir,targ_name)
    files=fnmatch.filter(os.listdir(orig_folder), '*.jpg')
    
    for file in files:
        try:
            orig_fname=file
            targ_fname=orig_fname.replace(orig_name,targ_name)
            os.rename(os.path.join(base_dir,orig_folder,orig_fname,),os.path.join(base_dir,orig_folder,targ_fname))
        except Exception as e:
            raise(f"Unexpected error for figure {file}: {e}")
    
    


for orig_name in orig_targ_dict.keys():
    targ_name=orig_targ_dict[orig_name]
    rename_folder_and_files(base_dir, orig_name, targ_name)

    os.rename(os.path.join(base_dir,orig_name),os.path.join(base_dir,targ_name))
###########
###########
import os
import fnmatch
import shutil
def seperate_160_to_80(basedir, src_dir_name):
    # Define source and destination folders
    src_folder=os.path.join(basedir, src_dir_name)
    dest_folder1=os.path.join(basedir, f'{src_dir_name}1')
    dest_folder2=os.path.join(basedir, f'{src_dir_name}2')

    # Ensure destination folders exist
    os.makedirs(dest_folder1, exist_ok=True)
    os.makedirs(dest_folder2, exist_ok=True)


    # Process files
    for i in range(1, 161):
        old_filename = f"{src_dir_name}-{i}.jpg"
        old_path = os.path.join(src_folder, old_filename)
        
        if not os.path.exists(old_path):
            print(f"Skipping missing file: {old_filename}")
            continue
        
        if i <= 80:
            new_filename = f"{src_dir_name}1-{i}.jpg"
            new_path = os.path.join(dest_folder1, new_filename)
        else:
            new_filename = f"{src_dir_name}2-{i-80}.jpg"
            new_path = os.path.join(dest_folder2, new_filename)
        
        shutil.move(old_path, new_path)
        print(f"Moved: {old_filename} -> {new_path}")

    print("Separation and renaming completed.")

homedir = os.getenv('HOME')
# if in linux, need to add one tlei
base_dir = os.path.join(homedir, "toolboxes/fLoc/stimuli")

langs=['CN'] #['AT','EN','ES','EU','FR','IT']
cats=['RW','CS','FF','SC']
folder_160 = [f"{code}_{cat}" for code in langs for cat in cats ]

for dir_name in folder_160:
    seperate_160_to_80(base_dir,dir_name)