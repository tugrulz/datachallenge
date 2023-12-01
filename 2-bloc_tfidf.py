import pandas as pd
# tokenize and then do tf-idf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def bloc_tokenizer(text):
    tokens = text.split('.')
    tokens = [token for token in tokens if token.strip()] # You can use any tokenization method you prefer
    return tokens


def create_tfidf(file, savefile):
    print((file, savefile))
    df = pd.read_csv(file)
    df['bloc'] = df['bloc_action'] + "." + df['bloc_content']
    vectorizer = TfidfVectorizer(tokenizer = bloc_tokenizer, ngram_range=(1, 1), min_df=0.005, max_df=0.90, lowercase=False)
    X = vectorizer.fit_transform(df['bloc'])
    feature_names = vectorizer.get_feature_names_out()
    X_array = X.toarray()
    tfidf_df = pd.DataFrame(X_array, columns=feature_names)
    tfidf_df['name'] = df['name']
    tfidf_df['total'] = df['total']
    tfidf_df.to_csv(savefile, index = False)

create_tfidf('output/bloc_1hour.csv', 'output/bloc_1hour_tfidf.csv')