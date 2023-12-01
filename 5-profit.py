import pandas as pd
df = pd.read_csv('data/challenge_problem_two_21NOV.csv', usecols = ['screen_name', 'follower_count'])
df = df[df.follower_count > 0]
follower_max = df.groupby('screen_name')['follower_count'].max().reset_index()
follower_max.columns = ['screen_name', 'follower_max']

follower_min = df.groupby('screen_name')['follower_count'].min().reset_index()
follower_min.columns = ['screen_name', 'follower_min']

df = follower_min.merge(follower_max, on = 'screen_name')
df['follower_diff'] = df['follower_max'] - df['follower_min']
df['ratio'] = df['follower_max'] / df['follower_min']
df['perc'] = df['follower_diff'] / df['follower_max']
df.to_csv('output/follower_gain.csv', index = False)