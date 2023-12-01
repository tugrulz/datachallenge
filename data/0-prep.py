'''

'''
import pandas as pd
import os
from tqdm import tqdm

dropped_columns = ['annotations', 'dataTags', 'extraAttributes', 'segments', 'geolocation',
                   'id', 'author', 'segments', 'id', 'translatedContentText', 'translatedTitle', 'name']
unnecessary_so_drop = ['title']

rename_cols = {'contentText':'text', 'timePublished':'created_at', 'language':'lang',
          'twitterData.engagementParentId':'linked_tweet',
          'twitterData.engagementType':'tweet_type',
          'twitterData.followerCount':'follower_count',
            'twitterData.followingCount':'following_count',
            'twitterData.likeCount':'like_count',
            'twitterData.retweetCount':'retweet_count',
            'twitterData.tweetId':'id',
               'embeddedUrls':'urls'}

def process(df):
    # get tweets than drop mediaType
    df = df.drop(columns=dropped_columns)
    df = df.drop(columns=unnecessary_so_drop)

    # get twitter only
    df = df[df['mediaType'] == 'Twitter']
    df = df.drop(columns = ['mediaType'])

    mediaTypeAttributes = pd.json_normalize(df['mediaTypeAttributes'])
    mediaTypeAttributes = mediaTypeAttributes[['twitterData.engagementParentId', 'twitterData.engagementType', 'twitterData.followerCount',
         'twitterData.followingCount', 'twitterData.likeCount', 'twitterData.retweetCount', 'twitterData.tweetId']]

    df = df.reset_index(drop=True)
    mediaTypeAttributes = mediaTypeAttributes.reset_index(drop=True)
    df = pd.concat([df, mediaTypeAttributes], axis=1)
    df = df.drop(columns=['mediaTypeAttributes'])

    # rename
    df = df.rename(columns=rename_cols)

    # created_at
    df['created_at'] = pd.to_datetime(df['created_at'], unit='ms')

    # http://twitter.com/Eye_On_Gaza/statuses/1697413595796328457
    df['screen_name'] = df.url.apply(lambda x: x.split('/')[-3])
    df = df.drop(columns=['url'])

    df = df.sort_index(axis=1)
    #
    df['linked_tweet'] = df.linked_tweet.astype(str)
    return df

os.chdir('data')
chunks = pd.read_json('challenge_problem_two_21NOV.jsonl', lines = True, chunksize = 100000)

for chunk in tqdm(chunks):
    df = process(chunk)
    if(os.path.exists('challenge_problem_two_21NOV.csv') == False):
        df.to_csv('challenge_problem_two_21NOV.csv', index=False)
    else:
        df.to_csv('challenge_problem_two_21NOV.csv', mode='a', header=False, index=False)
