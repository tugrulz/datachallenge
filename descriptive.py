import pandas as pd
df = pd.read_csv('data/challenge_problem_two_21NOV.csv', dtype = {'linked_tweet':str}, usecols = ['tweet_type', 'linked_tweet'])
df = df[df.tweet_type == 'reply']
a = df.linked_tweet.value_counts().reset_index()
a.columns = ['id', 'count']
a = a[a['count'] >= 5]
print(len(a))

# create cdf
a['cdf'] = a['count'].cumsum() / a['count'].sum()
# plot cdf with axis that increases by 50 in each step

import matplotlib.pyplot as plt
plt.plot(a['count'], a['cdf'])
step = 50
plt.xticks(range(min(a['count']), max(a['count']) + 1, step))
# step_minor = 25
# from matplotlib.ticker import MultipleLocator, NullFormatter
# minor_locator = MultipleLocator(25)
# plt.gca().xaxis.set_minor_locator(minor_locator)
# plt.gca().xaxis.set_minor_formatter(NullFormatter())

plt.yticks([i/10 for i in range(11)])
plt.grid(True)
plt.show()


#
#
# # make a histogram of reply counts
# import matplotlib.pyplot as plt
# plt.hist(a['count'], bins=[5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
# plt.show()
