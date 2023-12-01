'''
Create tsne from bloc_tfidf.csv
'''

import pandas as pd
import sklearn
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import classification_report, confusion_matrix, make_scorer, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

bloc_file = 'output/bloc_tfidf.csv'

# create tsne
def create_tsne(df):
    df = df.drop(['name', 'total'], axis = 1)
    X = df.to_numpy()
    X_embedded = TSNE(n_components=2, perplexity=30, n_iter=1000, learning_rate='auto', random_state=42).fit_transform(X)
    # X_embedded = PCA(n_components=2, random_state=42).fit_transform(X)
    return X_embedded

def create_PCA(df):
    df = df.drop(['name', 'total'], axis = 1)
    X = df.to_numpy()
    X_embedded = PCA(n_components=2, random_state=42).fit_transform(X)
    return X_embedded

# visualize tsne
def visualize_tsne(X_embedded, df):
    df['x'] = X_embedded[:,0]
    df['y'] = X_embedded[:,1]
    df.cluster = df.cluster.apply(lambda x: 1 if x == 0 else 0) # swap labels
    sns.scatterplot(data = df, x = 'x', y = 'y', hue = 'cluster')
    plt.show()

# create clusters
def create_clusters(X):
    clustering = KMeans(n_clusters=2, random_state=42).fit(X)
    # dbscan
    # clustering = DBSCAN(eps=0.5, min_samples=5).fit(X)
    df = pd.DataFrame([])
    df['x'] = X[:,0]
    df['y'] = X[:,1]
    df['cluster'] = clustering.labels_
    return df

# execute
df = pd.read_csv(bloc_file)
df = df[df.total >= 100]
X_embedded = create_tsne(df)
# X_embedded = create_PCA(df)
clusters = create_clusters(X_embedded)
df = df.reset_index(drop = True)
clusters = clusters.reset_index(drop = True)
df = pd.concat([df, clusters], axis = 1)
df.to_csv('output/bloc_tfidf_tsne.csv', index = False)
visualize_tsne(X_embedded, clusters)

# random forest to distinguish clusters
# swap labels if 0s are less
if(len(df[df.cluster == 0]) < len(df[df.cluster == 1])):
    df.cluster = df.cluster.apply(lambda x: 1 if x == 0 else 0) # swap labels
X = df.drop(['name', 'total', 'cluster', 'x', 'y'], axis = 1)
y = df['cluster']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42, stratify = y)
clf = RandomForestClassifier(max_depth=2, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
# feature analysis
feature_importances = pd.DataFrame(clf.feature_importances_,
                                      index = X_train.columns,
                                    columns=['importance']).sort_values('importance', ascending=False)
print(feature_importances)
