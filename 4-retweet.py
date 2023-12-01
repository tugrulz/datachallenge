import pandas as pd
df = pd.read_csv('./data/challenge_problem_two_21NOV_activeusers.csv', usecols = ['text', 'screen_name'])
names = set(df.screen_name)

df = df[df.text.str.startswith('RT @')]

#filter
cnt = df.screen_name.value_counts()
cnt = cnt[cnt >= 10]
names = set(cnt.index)

df['Target'] = df.text.str.split(' ').str[1].str.replace('@', '')
df = df.rename({'screen_name':'Source'}, axis = 1)
df = df[['Source', 'Target']]
df = df[df.Source != df.Target]
df = df[df.Target.isin(names)]
# Weight
df['Weight'] = 1
df = df.groupby(['Source', 'Target']).sum().reset_index()
print(len(df))
df.to_csv('output/retweet_forgephi_atleast10.csv', index = False)