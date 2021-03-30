"""
tmdb_api.py
~~~~~~~~~~~~
Used imdb id as input to get all the information in TMDB via API wrapper tmdbsimple
Wrapper API: https://github.com/celiao/tmdbsimple/
The code will do the following things:
    1. Read the IMDB id from mongoDB
    2. Get the basic movie information such as ratings, language, etc.
    3. Combine the basic information with credits information such as casts.
    4. Get the user reviews for all the movies.

Group AOLIGEI
"""
import tmdbsimple as tmdb
import json
import pandas as pd
import requests
#Preset global variables 
API_KEYS = '4e480f0d8ec5b4d36580cf622b9b6953'
POSTER_PREFIX = 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/'
tmdb.API_KEY = API_KEYS
GENRE_URL = f'https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEYS}&language=en-US'
genres_maps = requests.get(url = GENRE_URL).json()
genres_df = pd.DataFrame(genres_maps['genres'])
genres_df.index = genres_df.id

"""
Combine all the information from TMDB with IMDB id as input 
"""
def getInfoIMDB(imdb_id):
    imdb = tmdb.Find(imdb_id)
    results = imdb.info(external_source='imdb_id')
    isTv = len(results['movie_results']) == 0
    if all(len(v) == 0 for v in results.values()):
        # print(f'ERROR: The IMDB id: {imdb_id} return nothing')
        return None
    elif not isTv:
        all_info = parseFindBasic(results, imdb_id)
        movie = tmdb.Movies(all_info['id'])
        details = parseMovies(movie)
        all_info.update(details)
        more_info = parseMoreInfo(movie)
        all_info.update(more_info)
        mreview = getReviews(movie,all_info['id'],imdb_id)
        return (json.dumps(all_info),mreview)
    return None
    
"""
Parse the basic inforation with FIND() API call
FIND() will only return very basic information
"""
def parseFindBasic(responses, imdb_id):
    fdict = {}
    fdict['imdb_id'] = imdb_id
    attr_list = ['id', 'title', 'vote_average', 'vote_count', 'poster_path', \
                'genre_ids', 'original_language', 'popularity', 'release_date','original_title']
    for a in attr_list:
        fdict[a] =  responses['movie_results'][0][a]
    fdict['genre_ids'] = list(map(genre_map, fdict['genre_ids']))
    fdict['poster_path'] = POSTER_PREFIX + fdict['poster_path'][1:]
    fdict['overview'] =  responses['movie_results'][0]['overview']
    return fdict

"""
This function will map genre id to genre types
"""
def genre_map(g):
    if g in genres_df.index:
        return genres_df.loc[g]['name']
    else:
        return 'None'

"""
Parse the basic inforation with MOVIE() API call
MOVIE() will only return more detailed information
"""
def parseMovies(movie):
    attr_list = ['budget', 'revenue', 'runtime', 'status', 'tagline','adult','homepage']
    mdict = {}
    movie = movie.info()
    for a in attr_list:
        mdict[a] = movie[a]
    mdict['company_id'] = [i['id'] for i in movie['production_companies']]
    mdict['company_name'] = [i['name'] for i in movie['production_companies']]
    # print(mdict)
    return mdict

"""
Used functions like keywords, credit, to get more information
"""
def parseMoreInfo(movie):
    midict = {}
    keywords = movie.keywords()
    midict['keywords_id'] = [i['id'] for i in keywords['keywords']]
    midict['keywords_name'] = [i['name'] for i in keywords['keywords']]
    cast = movie.credits()['cast']
    df = pd.DataFrame(cast)
    midict['num_of_cast'] = len(df.index)
    top_10_cast = df.sort_values(['popularity'], ascending=False).head(10)
    midict['top_10_cast_popularity_mean'] = top_10_cast['popularity'].mean()
    midict['casts'] = top_10_cast.head(5)['name'].tolist()
    midict['top_5_cast_popularity'] = top_10_cast.head(5)['popularity'].tolist()

    crew = movie.credits()['crew']
    df = pd.DataFrame(crew)
    df = df.drop_duplicates(subset=['name'])
    top_10_crew = df.sort_values(['popularity'], ascending=False).head(10)
    midict['top_10_crew_popularity_mean'] = top_10_crew['popularity'].mean()
    midict['crews'] = top_10_crew['name'].tolist()
    midict['top_10_crew_popularity'] = top_10_crew['popularity'].tolist()
    hasDirector = top_10_crew[top_10_crew['job'] == 'Director']['name'].count() > 0
    if hasDirector:
        director = top_10_crew[top_10_crew['job'] == 'Director']['name'].values[0]
    else:
        director = 'None'
    midict['director'] = director
    return midict

"""
Get all the user reviews with movie id as an input
"""
def getReviews(movie, tmdb, imdb):
    reviews = movie.reviews()
    all_review = {'id': tmdb,'imdb_id': imdb}
    mre = []
    for r in reviews['results']:
        rdict = {}
        rdict['author'] = r['author']
        rdict['rating'] = r['author_details']['rating']
        rdict['content'] = r['content']
        rdict['url'] = r['url']
        mre.append(rdict)
    all_review['review'] = mre
    return json.dumps(all_review)



"""
Return NONE if API return nothing or is a TV shows.
getInfoIMDB(imdb_id) will return basic movie information and movie reviews
"""
if __name__ == '__main__':
    # imdb_id = 'tt5491994'
    imdb_id = 'tt12361974'
    results = getInfoIMDB(imdb_id)
    if results != None:
        minfo, mreview = results
        print(minfo)
        print()
        print(mreview)


