import numpy as np
import scipy.sparse
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def get_sparse(vector):
    cosine_similarities = cosine_similarity(vector, vector)
    np.percentile( cosine_similarities[:,0],1)

    cos_dist_df = pd.DataFrame(cosine_similarities)
    cos_dist_df[cos_dist_df>1.5] = 0

    # make sparse matrix
    sparse_mat = scipy.sparse.csc_matrix(cos_dist_df)


    return sparse_mat


def movie_recommendations(sparse_mat,df,title):
    movies = df[df['isMovie']==1]['title']
    #Reverse mapping of the index
    indices = pd.Series(df.index, index = df['title'])
    idx = indices[title]

    result = pd.DataFrame(sparse_mat[:,idx].toarray()).sort_values(by=0,ascending=False).head(20).index
    movie_indices  = [score for score in result if df.iloc[score]['isMovie']==1]
    movie_indices = movie_indices[0:5]

    print(movie_indices)
    recommend = movies.iloc[movie_indices]
    return recommend,movie_indices,idx

def book_recommendations(sparse_mat,df,title):


    books = df[movie_book_df2['isMovie']==0]['title']
    #Reverse mapping of the index
    indices = pd.Series(df2.index, index = df['title'])
    idx = indices[title]


    result = pd.DataFrame(sparse_mat[:,idx].toarray()).sort_values(by=0,ascending=False).index
    book_indices  = [score for score in result if movie_book_df2.iloc[score]['isMovie']==0]
    book_indices = movie_indices[0:5]

    print(movie_indices)
    recommend = books.loc[book_indices]
    return recommend,book_indices,idx

def get_vectors(x,model):

    global word_embeddings
    word_embeddings = []

    # Reading the each book description
    for line in x:
        avgword2vec = None
        count = 0
        for word in line.split():
            #print(word)
            if word in model:
                count += 1
                if avgword2vec is None:
                    avgword2vec = model[word]
                else:
                    avgword2vec = avgword2vec + model[word]

        if avgword2vec is not None:
            avgword2vec = avgword2vec / count

            word_embeddings.append(avgword2vec)
