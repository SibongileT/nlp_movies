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


    books = df[df['isMovie']==0]['title']
    #Reverse mapping of the index
    indices = pd.Series(df.index, index = df['title'])
    idx = indices[title]


    result = pd.DataFrame(sparse_mat[:,idx].toarray()).sort_values(by=0,ascending=False).index
    book_indices  = [score for score in result if df.iloc[score]['isMovie']==0]
    book_indices = book_indices[0:5]

    recommend = books.loc[book_indices]
    return recommend,book_indices,idx


def word2vec_recommendations(title,df,cosine_similarities):



    # taking the title and book image link and store in new data frame called books
    movies = df[df['isMovie']==1][['title','author/director','release_date']]
    #books = movie_book_df['title']
    #Reverse mapping of the index
    indices = pd.Series(df.index, index = df['title'])
    print(len(indices))

    idx = indices[title]
    sim_scores = list(enumerate(cosine_similarities[idx]))
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    sim_scores  = [score for score in sim_scores if df.iloc[score[0]]['isMovie']==1]
    sim_scores = sim_scores[1:6]
    print(sim_scores)
    movie_indices = [i[0] for i in sim_scores]
    print(movie_indices)
    recommend = movies.iloc[movie_indices]
    return recommend
