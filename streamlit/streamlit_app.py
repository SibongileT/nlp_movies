import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pickle

st.title('Book Movie Recommender')



page_bg_img = '''
<style>
body{
background-color: linear-gradient(
rgba(241, 233, 219, 0.2),rgba(241, 233, 219, 0.2)
);
background: url("https://images.unsplash.com/photo-1540924817141-d963bdafed69?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2851&q=80");
background-size: cover;
}
table{
background-color:#E8E8E8;
}

</style>
'''

movie_book_df = pd.read_pickle('sample_data2.pkl')
book_df = pd.read_pickle('book_info.pkl')
sparse_mat = pickle.load(open("sparse.pkl",'rb'))

st.markdown(page_bg_img,unsafe_allow_html=True)
add_radio = st.sidebar.radio(
    "Do you want to be recommended a book or movie?",
    ('Movie', 'Book')
)
if add_radio=='Movie':
    book_list = []
    for book in book_df.iloc[:1000].title:
        book_list.append(book.title())
    title = st.selectbox(
        'What book would you like some movies for?',
        book_list
    )

    st.markdown(page_bg_img,unsafe_allow_html=True)

    @st.cache
    def recommendations(title,num):
        # finding cosine similarity for the vectors
        #cosine_similarities = cosine_similarity(tf_result,tf_result)
        # taking the title and book image link and store in new data frame called books
        movies = movie_book_df[movie_book_df['isMovie']==1][['title','author/director','release_date']]
        #books = movie_book_df['title']
        #Reverse mapping of the index
        indices = pd.Series(movie_book_df.index, index = movie_book_df['title'])
        idx = indices[title]

        #sim_scores = list(enumerate(cosine_similarities[idx]))


        result = pd.DataFrame(sparse_mat[:,idx].toarray()).sort_values(by=0,ascending=False).head(20).index
        movie_indices  = [score for score in result if movie_book_df.iloc[score]['isMovie']==1]
        movie_indices = movie_indices[0:num]
        print(movie_indices)
        sim_movies = []
        directors = []
        release_date=[]
        sim_movies=movies.iloc[movie_indices]['title']
        directors = movies.iloc[movie_indices]['author/director']
        release_date = movies.iloc[movie_indices]['release_date']
        return pd.DataFrame(list(zip(sim_movies, directors,release_date)),columns=['Movie','Director','Release Date']),movie_indices,idx

    num = st.sidebar.slider("set value", min_value=1, value=5, max_value=10)
    df,movie_indices,title_idx = recommendations(title.lower(),num)
    option1, option2, usertext1 = False, False, "default_text"
    if st.button("submit"):
        option1 = True
        st.table(df)

if add_radio=='Book':
    movie_list = []
    for movie in movie_book_df.title:
        if not movie.islower():
            movie_list.append(movie.title())
    title = st.selectbox(
        'What movie would you like some books for?',
        movie_list
    )

    st.markdown(page_bg_img,unsafe_allow_html=True)

    @st.cache
    def recommendations(title,num):

        movies = movie_book_df[movie_book_df['isMovie']==0][['title','author/director']]

        #Reverse mapping of the index
        indices = pd.Series(movie_book_df.index, index = movie_book_df['title'])
        idx = indices[title]

        #sim_scores = list(enumerate(cosine_similarities[idx]))


        result = pd.DataFrame(sparse_mat[:,idx].toarray()).sort_values(by=0,ascending=False).head(50).index
        movie_indices  = [score for score in result if movie_book_df.iloc[score]['isMovie']==0]
        movie_indices = movie_indices[0:num]
        print(movie_indices)
        sim_movies = []
        directors = []
        sim_movies=movies.loc[movie_indices]['title'].str.title()
        directors = movies.loc[movie_indices]['author/director']
        return pd.DataFrame(list(zip(sim_movies, directors)),columns=['Book','Author']),movie_indices,idx

    num = st.sidebar.slider("set value", min_value=1, value=5, max_value=10)
    df,movie_indices,title_idx = recommendations(title,num)
    if st.button("submit"):
        st.table(df)
