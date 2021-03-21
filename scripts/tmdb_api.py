"""
tmdb_api.py
~~~~~~~~~~~~
Used imdb id as input to get all the information in TMDB via API wrapper tmdbsimple
Wrapper API: https://github.com/celiao/tmdbsimple/

Group AOLIGEI
"""
import tmdbsimple as tmdb
import json
import pandas as pd
imdb_id = 'tt0795176'
imdb_id = 'tt0198781'
#Preset global variables 
API_KEYS = '4e480f0d8ec5b4d36580cf622b9b6953'
POSTER_PREFIX = 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/'
tmdb.API_KEY = API_KEYS

"""
Get the basic moive information from TMDB with IMDB id as input 
"""
def getBasicInfoIMDB(imdb_id):
    imdb = tmdb.Find(imdb_id)
    results = imdb.info(external_source='imdb_id')
    if all(len(v) == 0 for v in results.values()):
        print(f'ERROR: The IMDB id: {imdb_id} return nothing')
    else:
        parseBasic(results)

"""
Parse the basic inforation and return id for the following API calls 
"""
def parseBasic(responses):
    isTv = len(responses['movie_results']) == 0
    fdict = {}
    fdict['isTv'] = isTv
    tvMapToMovie = {
        'name': 'title',
        'first_air_date': 'release_date'
    }
    keys = tvMapToMovie.values()
    attr = 'movie_results'
    attr_list = ['id', 'vote_average', 'vote_count', 'poster_path', \
                'genre_ids', 'original_language', 'popularity']
    if isTv:
        attr = 'tv_results'
        keys = tvMapToMovie.keys()
    for a in attr_list:
        fdict[a] =  responses[attr][0][a]
    fdict['poster_path'] = POSTER_PREFIX + fdict['poster_path'][1:]
    for k in keys:
        fdict[k] =  responses[attr][0][k]
    fdict['overview'] =  responses[attr][0]['overview']
    return fdict['id']
    
    # print(responses['movie_results'])
if __name__ == '__main__':
    getBasicInfoIMDB(imdb_id)

