import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

df = pd.read_csv('./data/challenge_problem_two_21NOV_activeusers.csv', usecols = ['screen_name', 'linked_tweet'], keep_default_na=False)
df = df[df.linked_tweet != 'None']

def filter_majority(): # nizzolis way.. do we need it tho?
    a = df.screen_name.value_counts()
    cumulative = a.cumsum()
    total_tweets = a.sum()
    return cumulative[cumulative <= total_tweets*0.5].index


id_corpus = df.groupby('screen_name')['linked_tweet'].agg(lambda x: ' '.join(x)).reset_index()
id_corpus.columns = ['screen_name', 'linked_tweet_corpus']

vectorizer = TfidfVectorizer(min_df=0.0005)
tfidf_matrix = vectorizer.fit_transform(id_corpus['linked_tweet_corpus'])
cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
for i in range(len(id_corpus)):
    cosine_sim_matrix[i,i]=0

tuples = []

# create pandas dataframe from cosine similarity matrix with 3 columns
cosine_sim_df = pd.DataFrame(np.triu(cosine_sim_matrix, k=1), columns=range(1, cosine_sim_matrix.shape[0]+1), index=range(1, cosine_sim_matrix.shape[0]+1)).stack().reset_index()
cosine_sim_df.columns = ['Source_index', 'Target_index', 'Weight']
cosine_sim_df = cosine_sim_df[cosine_sim_df.Weight >= 0.1]

id_corpus = id_corpus.reset_index().drop('linked_tweet_corpus', axis=1)
id_corpus.columns = ['Target_index', 'Target']
cosine_sim_df = cosine_sim_df.merge(id_corpus, on = 'Target_index')
id_corpus.columns = ['Source_index', 'Source']
cosine_sim_df = cosine_sim_df.merge(id_corpus, on = 'Source_index')
cosine_sim_df = cosine_sim_df[['Source', 'Target', 'Weight']]

print(len(cosine_sim_df))
cosine_sim_df.to_csv('output/cosine_sim_min02.csv', index=False)

