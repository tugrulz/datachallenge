import pandas as pd
# no anomaly detection version

df = pd.read_csv('data/challenge_problem_two_21NOV.csv', usecols = ['screen_name', 'linked_tweet'])
df = df[df.linked_tweet != 'None']

a = df.screen_name.value_counts().reset_index()
a.columns = ['screen_name', 'rt_count']

linked = df.linked_tweet.value_counts()
linked = linked[linked > 10].index
df = df[df.linked_tweet.isin(linked)]
df = df.merge(a, on = 'screen_name')
avg_rt_count = df.groupby('linked_tweet')['rt_count'].mean().reset_index()
avg_rt_count.columns = ['id', 'avg_rt_count_of_authors']
avg_rt_count['id'] = avg_rt_count.id.astype(int)

df = pd.read_csv('data/challenge_problem_two_21NOV.csv', usecols = ['screen_name', 'id', 'text', 'retweet_count'])
df = df.merge(avg_rt_count, on = 'id')
df.to_csv('output/retweet_anomaly_nodetection.csv', index = False)

