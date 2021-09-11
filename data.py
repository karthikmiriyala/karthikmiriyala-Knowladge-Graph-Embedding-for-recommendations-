import numpy as np
import pandas as pd
movies=pd.read_csv('movies.dat',sep='::',header=None,names=['MovieId','Title','Genres'],engine='python')
ratings=pd.read_csv('ratings.dat',sep='::',header=None,names=['UserId','MovieId','Rating','Timestamp'],engine='python')
users=pd.read_csv('users.dat',sep='::',header=None,names=['UserId','Gender','Age','Occupation','Zip-code'],engine='python')

#movies
import re

movies['movie_year'] = movies['Title']

movies['movie_year'] = movies['movie_year'].str.extract(r"\(([0-9]+)\)", expand=False)

# creating a new column with just the movie titles
movies['movie_title'] = movies['Title']
movies['movie_title'] = movies['movie_title'].str.extract('(.*?)\s*\(', expand=False)
movies['Title'] = movies['movie_title']
movies.drop(['movie_title'],axis=1,inplace=True)

def genres_splitter(data):
    l ={}
    l['Title'] = []
    l['Genres'] = []
    for index,row in data.iterrows():
        try:
            genres = row.Genres.split('|')
            for i in range(len(genres)):
                l['Title'].append(row.Title)
            l['Genres'].extend(genres)
        except:
            l['Title'].append(row.Title)
            l['Genres'].extend(row.Genres)
    return pd.DataFrame(l)

users['Age_Group']=np.nan
users.loc[users['Age'] ==1, 'Age_Group'] = 'Under 18'
users.loc[users['Age'] ==18, 'Age_Group'] = '18-24'
users.loc[users['Age'] ==25, 'Age_Group'] = '25-34'
users.loc[users['Age']==35, 'Age_Group'] = '35-44'
users.loc[users['Age'] ==45, 'Age_Group'] = '45-49'
users.loc[users['Age'] ==50, 'Age_Group'] = '50-55'
users.loc[users['Age']==56, 'Age_Group'] = '56+'



# data_ru=pd.merge(ratings,users[['UserId','Gender','Age','Age_Group','Occupation']],
#              on='UserId',how='inner')
# data=pd.merge(data_ru[['UserId','MovieId','Rating','Gender','Age_Group','Age','Occupation']],
#               movies[['Title','Genres','movie_year']],on='MovieId',
#             how='inner')


#dropping columns
# data.drop(['MovieId','Age'],inplace=True,axis=1)


########################
# Triplets
movielens_triplets = pd.DataFrame(data = None,columns=['subject','object','predicate'])
# <h1> 1. Movies: <h1>
    # movie_Title --> Released in --> year
df = pd.DataFrame()
df['subject']= movies['Title']
df['object'] = 'Released in'
df['predicate'] = movies['movie_year']
movielens_triplets = movielens_triplets.append(df)
# movie_title --> Genres --> Genres
df = pd.DataFrame()
g = genres_splitter(movies)
df['subject']= g['Title']
df['object'] = 'Genres'
df['predicate'] = g['Genres']
movielens_triplets = movielens_triplets.append(df)

#############################################
# 2. Users :
# UserId --> Gender --> Gender
df = pd.DataFrame()
df['subject']= users['UserId']
df['object'] = 'Gender'
df['predicate'] = users['Gender']
movielens_triplets = movielens_triplets.append(df)
# UserId --> Occupation --> Occupation
df = pd.DataFrame()
df['subject']= users['UserId']
df['object'] = 'Occupation'
df['predicate'] = users['Occupation']
movielens_triplets = movielens_triplets.append(df)
# UserId --> Age Group --> Age Group
df = pd.DataFrame()
df['subject']= users['UserId']
df['object'] = 'Age_Group'
df['predicate'] = users['Age_Group']
movielens_triplets = movielens_triplets.append(df)

############################
# 3. ratings
# UserId --> watched --> Title
l=dict()
z = []
for k, val in zip(movies['MovieId'].values,movies['Title'].values):
    l[k]=val
for x in ratings['MovieId']:
    z.append(l.get(x))
ratings['Title'] = z
df = pd.DataFrame()
df['subject']= ratings['UserId']
df['object'] = 'Watched'
df['predicate'] = ratings['Title']
movielens_triplets = movielens_triplets.append(df)
# UserId --> Title/rating --> Rating
df = pd.DataFrame()
df['subject']= ratings['UserId']
df['object'] = ratings['Title']+'/Rating'
df['predicate'] = ratings['Rating']
movielens_triplets = movielens_triplets.append(df)

np.save('movielens_triplets.npy',movielens_triplets,allow_pickle=True)


