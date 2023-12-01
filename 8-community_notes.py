import pandas as pd
from tqdm import tqdm

# community noted tweets sadece original tweetlerden mi ona bak

# def create_dataframe():
def create():
    df = pd.read_csv('data/challenge_problem_two_21NOV.csv', usecols = ['id', 'created_at', 'linked_tweet', 'text', 'screen_name', 'tweet_type'])
    original = df[df.tweet_type != 'retweet']

    df = df[df.linked_tweet != 'None']
    df['linked_tweet'] = df.linked_tweet.astype(int)
    a = df.linked_tweet.value_counts()
    a = a[a > 10].index
    ids = set(a)

    df = df[df.linked_tweet.isin(ids)]
    df['screen_name'] = df.text.str.split(' ').str[1].str.replace('@', '')
    df['text'] = df.text.str.split(' ').str[2:].str.join(' ')
    df['id'] = df.linked_tweet
    df = df.drop('linked_tweet', axis = 1)

    original = original[original.id.isin(ids)]
    original = original.drop('linked_tweet', axis = 1)

    original['original'] = True
    df['original'] = False

    df = pd.concat([original, df])
    df = df.sort_values(['id', 'created_at'])

    comm = pd.read_csv('data/community_noted_tweets.csv', usecols = ['id', 'note_created_at', 'classification'])
    comm['misleading'] = 0
    comm.loc[comm.classification == 'MISINFORMED_OR_POTENTIALLY_MISLEADING', 'misleading'] = 1
    comm.loc[comm.classification == 'NOT_MISLEADING', 'misleading'] = -1
    comm_misleading = comm.groupby('id')['misleading'].sum().reset_index()
    comm_misleading['misleading'] = comm_misleading.misleading.apply(lambda x: 1 if x > 0 else 0)

    comm_first_noted = comm.groupby('id')['note_created_at'].min().reset_index()
    comm_first_noted.columns = ['id', 'first_noted']
    comm_first_noted['first_noted'] = pd.to_datetime(comm_first_noted.first_noted.apply(lambda x: x.split('.')[0]))
    comm = comm_first_noted.merge(comm_misleading, on = 'id')

    df['id'] = df.id.astype(int)
    backup = df
    df = df.merge(comm, on = 'id', how = 'left')
    df['misleading'] = df.misleading.fillna(-1)
    df['first_noted'] = df.first_noted.fillna(df['created_at'])
    df.to_csv('output/popular_tweets.csv', index = False)

df = pd.read_csv('output/popular_tweets.csv')
df['first_noted'] = pd.to_datetime(df.first_noted.apply(lambda x: x.split('.')[0]))
df['created_at'] = pd.to_datetime(df.created_at)
df['time_before_first_noted'] = df['first_noted'] - df['created_at']
df['time_before_first_noted'] = df.time_before_first_noted.dt.total_seconds() / 3600

mean_note = df[(df['time_before_first_noted'] > 0) & (df.original == True)].time_before_first_noted.mean()
median_note = df[(df['time_before_first_noted'] > 0) & (df.original == True)].time_before_first_noted.median()

original = df[df.original == True]
engagaments = df[df.original == False]

original_ids = list(set(original.id))

tuples = []

for id in tqdm(original_ids):
    original_tweet = original[original.id == id]
    engagaments_tweet = engagaments[engagaments.id == id]
    misleading = original_tweet.misleading.values[0]
    total = len(engagaments_tweet)

    created_at_plus_mean_note = original_tweet.created_at.values[0] + pd.Timedelta(seconds = mean_note * 3600)
    created_at_plus_median_note = original_tweet.created_at.values[0] + pd.Timedelta(seconds = median_note * 3600)
    first_noted = original_tweet.first_noted.values[0]

    engagements_before_first_noted = len(engagaments_tweet[engagaments_tweet.created_at <= first_noted])
    engagements_before_mean = len(engagaments_tweet[engagaments_tweet.created_at <= created_at_plus_mean_note])
    engagements_before_median = len(engagaments_tweet[engagaments_tweet.created_at <= created_at_plus_median_note])

    engagements_after_first_noted = len(engagaments_tweet[engagaments_tweet.created_at > first_noted])
    engagements_after_mean = len(engagaments_tweet[engagaments_tweet.created_at > created_at_plus_mean_note])
    engagements_after_median = len(engagaments_tweet[engagaments_tweet.created_at > created_at_plus_median_note])

    tuples.append((id, misleading, total, engagements_before_first_noted, engagements_before_mean, engagements_before_median, engagements_after_first_noted, engagements_after_mean, engagements_after_median))

output = pd.DataFrame(tuples, columns = ['id', 'misleading', 'total', 'engagements_before_first_noted', 'engagements_before_mean', 'engagements_before_median', 'engagements_after_first_noted', 'engagements_after_mean', 'engagements_after_median'])
output.to_csv('output/popular_tweets_community_notes_engagement_analysis.csv', index = False)






# original['time_before_first_noted_amputed_with_median'] = original['time_before_first_noted']
# original[original['time_before_first_noted'] > 0, 'time_before_first_noted_amputed_with_median'] = median_note
#
# original['time_before_first_noted_amputed_with_mean'] = original.time_before_first_noted
# original[original['time_before_first_noted'] > 0, 'time_before_first_noted_amputed_with_mean'] = mean_note


