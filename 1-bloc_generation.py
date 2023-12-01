# bloc model
import pandas as pd
import numpy as np
from glob import glob
from tqdm import tqdm
import os
import multiprocessing as mp
df = pd.read_csv('data/challenge_problem_two_21NOV_activeusers.csv', dtype = {'linked_tweet':str})
df['created_at'] = pd.to_datetime(df['created_at'])
df = df.sort_values(by=['screen_name', 'created_at'])

PAUSE = pd.Timedelta(minutes=60)

def extract_user_mentions(text):
    if(text.startswith('RT @')):
        text = ' '.join(text.split(' ')[2:])
    return [x.split('@')[1] for x in text.split(' ') if x.startswith('@')]

def extract_hashtags_for_control(text):
    mentions = [x.split('#')[1] for x in text.split(' ') if x.startswith('#')]
    return mentions

df['mentions'] = df.text.apply(extract_user_mentions)
df['hashtags'] = df.text.apply(extract_hashtags_for_control)

def action_alphabet(row):
    if(row['tweet_type'] == 'retweet'):
        retweeted_user = row['text'].split('@')[0].split(':')[-1]
        if(retweeted_user == row['screen_name']):
            return '€'
        else:
            return 'r'
    elif(row['tweet_type'] == 'reply'):
        try:
            replied_user = row['text'].split('@')[1].split(' ')[0]
        except:
            return 't'
        if(replied_user == row['screen_name']):
            return 'π'
        else:
            return 'p'
    else:
        return 't'

def content_alphabeth(row):
    content = 'T'

    try: content += len(row['hashtags'])*'H'
    except:pass

    try: content += len(row['mentions'])*'@'
    except:pass

    try: content += len(eval(row['urls']))*'U'
    except:pass

    try: content += len(eval(row['imageUrls']))*'M'
    except:pass

    if(row['tweet_type'] == 'quote'):
        content += 'Q'
    return content

def create_bloc(df):
    pd.DataFrame([], columns=['name', 'total', 'bloc_action', 'bloc_content']).to_csv('output/bloc_1hour.csv', index=False)
    for screen_name, df_screen_name in tqdm(df.groupby('screen_name')):
        total = len(df_screen_name)

        cur_time = 0
        bloc_action = ""
        bloc_content = ""

        for i, row in df_screen_name.iterrows():
            # add pause
            if (cur_time == 0):
                cur_time = row['created_at']  # first time
            elif (row['created_at'] - cur_time > PAUSE):
                bloc_action += "."
            cur_time = row['created_at']

            # add action alphabet
            bloc_action += action_alphabet(row)
            bloc_content += content_alphabeth(row) + "."
        # tuples.append((screen_name, total, bloc_action, bloc_content))
        df = pd.DataFrame([[screen_name, total, bloc_action, bloc_content]], columns=['name', 'total', 'bloc_action', 'bloc_content'])
        df.to_csv('output/bloc_1hour.csv', index=False, mode = 'a', header=False)
    # df = pd.DataFrame(tuples, columns=['name', 'total', 'bloc_action', 'bloc_content'])
    # df.to_csv('output/bloc.csv', index=False)

if __name__ == '__main__':
    create_bloc(df)