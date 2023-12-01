import pandas as pd
import os
from tqdm import tqdm

df = pd.read_csv('./challenge_problem_two_21NOV.csv', usecols = ['screen_name'])
a = df.screen_name.value_counts()
a = set(a[a >= 10].index)
print()
chunks =  pd.read_csv('./challenge_problem_two_21NOV.csv', dtype = {'linked_tweet':str}, chunksize = 100000)
for df in tqdm(chunks):
    df = df[df.screen_name.isin(a)]
    if(os.path.exists('./challenge_problem_two_21NOV_activeusers.csv') == False):
        df.to_csv('./challenge_problem_two_21NOV_activeusers.csv', index=False)
    else:
        df.to_csv('./challenge_problem_two_21NOV_activeusers.csv', mode='a', header=False, index=False)