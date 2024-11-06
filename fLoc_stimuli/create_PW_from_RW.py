from wuggy import WuggyGenerator
import random
import pandas as pd
import os
import time

def gen_PW(df_RWH, df_RWL, df_word_col_name ,lang):
    '''
    code for generating PW list from word

    need to input RWH list and RWL list

    It will take half of the RWH and half of the RWL to form the final PW
    
    lang: valid options: english, italian, french, german
    '''
    g = WuggyGenerator()
    g.load(f"orthographic_{lang}")
    mixed_df, word_list=gen_rand_word_list(df_RWH, df_RWL,df_word_col_name)
    rw_pw_pair_lst=[]
    t=time.time()
    for word in word_list:
        try:    
            pw_lst=[]
            for match in g.generate_classic([word]):
                pw_lst.append(match["pseudoword"])
            num_ps=len(pw_lst)
            rand_idx= random.sample(range(0,num_ps),1)
            ps_word= pw_lst[rand_idx[0]]
            rw_pw_pair_lst.append((match['word'],ps_word))
        except Exception:
            print(f"One {word} in the MIXED list is wrong, but we excluded it into the final list")
        
    elapsed = time.time() - t
    print(f'Time take to get the PW df is {elapsed}')   
    rw_pw_df,pw_df=gen_output(rw_pw_pair_lst)

    return mixed_df, rw_pw_df, pw_df

def gen_rand_word_list(df_RWH, df_RWL, word_col_name):
    
    # randomize gen index of 50 RWH and 50 RHL
    rand_high_idx=random.sample(range(0, df_RWH.shape[0]),50)
    rand_low_idx=random.sample(range(0, df_RWL.shape[0]),50)
    rand_high_df=df_RWH.iloc[rand_high_idx]
    rand_low_df=df_RWL.iloc[rand_low_idx]

    mixed_df=pd.concat([rand_high_df,rand_low_df],axis=0)
    word_list=mixed_df[word_col_name].tolist()
    return mixed_df,word_list

def gen_output(rw_pw_tuple_list):
    '''
    '''
    rw_pw_df=pd.DataFrame(rw_pw_tuple_list,columns=['RW','PW'])
    pw_df=rw_pw_df['PW']
    return rw_pw_df,pw_df

def main():
    basedir='/Users/tiger/toolboxes/votc-langorth/fLoc_stimuli/Italian'
    RWH_fname='IT_RWH.txt' 
    RWL_fname='IT_RWL.txt'

    df_RWH=pd.read_csv(os.path.join(basedir,RWH_fname))
    df_RWL=pd.read_csv(os.path.join(basedir,RWL_fname))

    ref_rw_df, rw_pw_df, pw_df=gen_PW(df_RWH,df_RWL,"LEMMA",'italian')
    # then save both dataframe 
    ref_df_fname=os.path.join(basedir,'IT_mixed_RWHL.txt')
    rw_pw_list_fname=os.path.join(basedir,'IT_RW_PW_match.txt')
    pw_txt_fname=os.path.join(basedir,'IT_PW.txt')

    ref_rw_df.to_csv(ref_df_fname,sep='\t', index=False)
    rw_pw_df.to_csv(rw_pw_list_fname, sep='\t',index=False)
    pw_df.to_csv(pw_txt_fname,sep='\t', index=False)
    print(f'Length of the PW list is {pw_df.shape[0]}')
    
if __name__ =='__main__':
    main()