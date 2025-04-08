import os
import pandas as pd

basedir = '/home/tlei/tlei/toolboxes/votc-langorth/DATA/FR_material'

# Load FR_RW
rw_path = os.path.join(basedir, 'FR_RW.txt')
rw = pd.read_csv(rw_path, header=0)

# Load FR_RWH and FR_RWL
rwh_path = os.path.join(basedir, 'FR_RWH.txt')
rwl_path = os.path.join(basedir, 'FR_RWL.txt')

rwh = pd.read_csv(rwh_path, header=0)
rwl = pd.read_csv(rwl_path, header=0)

# Assuming the first column contains the word list (adjust if it's another column name)
rw_words = set(rw.iloc[:, 0])
rwh_words = set(rwh.iloc[:, 0])
rwl_words = set(rwl.iloc[:, 0])

# Get the difference: what's in RWH and RWL but not in RW
rwh_remaining = rwh_words - rw_words
rwl_remaining = rwl_words - rw_words

# Combine remaining words into a new list
new_list = list(rwh_remaining.union(rwl_remaining))

# Print how many come from each source
print(f"New list has {len(new_list)} words total.")
print(f" - {len(rwh_remaining)} from RWH")
print(f" - {len(rwl_remaining)} from RWL")

# Save the new list to a file (optional)
new_list_path = os.path.join(basedir, 'FR_remaining.txt')
with open(new_list_path, 'w') as f:
    for word in new_list:
        f.write(f"{word}\n")


# now I need to create new RWH and RHL for FR so that the PW code can work

# Assume the first column contains the word list
rw_words = set(rw.iloc[:, 0])
rwh_words = set(rwh.iloc[:, 0])
rwl_words = set(rwl.iloc[:, 0])

# Remove RW words from each list separately
rwh_cleaned = list(rwh_words - rw_words)
rwl_cleaned = list(rwl_words - rw_words)

# Create DataFrames with column 'lemma'
rwh_df = pd.DataFrame({'lemma': rwh_cleaned})
rwl_df = pd.DataFrame({'lemma': rwl_cleaned})

# Save to new files
rwh_df.to_csv(os.path.join(basedir, 'FR_RWH2.txt'), index=False)
rwl_df.to_csv(os.path.join(basedir, 'FR_RWL2.txt'), index=False)
