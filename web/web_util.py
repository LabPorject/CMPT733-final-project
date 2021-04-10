import pandas as pd 
import numpy as np
import random
from datetime import date
import requests
from pandas.tseries.holiday import USFederalHolidayCalendar
FILE_DIR = '../pred_lists'
API_KEYS = '4e480f0d8ec5b4d36580cf622b9b6953'

def getPopularity(name):
    name = name.replace(' ', '%20')
    tmdb_urls = f'https://api.themoviedb.org/3/search/person?api_key={API_KEYS}&language=en-US&query={name}&page=1&include_adult=false'
    r = requests.get(url = tmdb_urls)
    if r.status_code != 200:
        return 0.0
    else:
        res = r.json()
        if 'results' in res.keys():
            if (len(res['results']) >= 1):
                data = res['results'][0]
                if 'popularity' in data.keys():
                    return data['popularity']
    return 0

def random_input(isGood):
    num_genres = random.randint(1, 4)
    primaryTitle = pd.read_csv(f"{FILE_DIR}/movie_names.csv").sample(n = 1)['name'].tolist()[0]
    genres = pd.read_csv(f"{FILE_DIR}/genres_list.csv").sample(n = int(num_genres))['genres'].tolist()
    originalTitle = primaryTitle
    isAdult = random.randint(0, 1)
    release_year_int = float(random.randint(2000, 2021))
    runtimeMinutes = random.uniform(70.0, 120.0)
    if isGood == True:
        genres_list = ['Documentary', 'History', 'War', 'Music']
        genres = random.sample(genres_list, num_genres)
        Directors = pd.read_csv(f"{FILE_DIR}/top_director_list.csv").sample(n = 3)['Directors'].tolist()
        Writers = pd.read_csv(f"{FILE_DIR}/top_Writers_list.csv").sample(n = 3)['Writers'].tolist()
        num_of_crew = random.randint(1, 9)
        crews_df = pd.read_csv(f"{FILE_DIR}/tops_crews_list.csv")
        crews = crews_df.sample(n = num_of_crew)['crews'].tolist()
        crews_df.set_index('crews',inplace=True)
        num_of_cast = random.randint(4, 10)
        casts_df = pd.read_csv(f"{FILE_DIR}/tops_casts_list.csv")
        casts = casts_df.sample(n = num_of_cast)['casts'].tolist()
        casts_df.set_index('casts',inplace=True)
        top_10_cast_popularity = [casts_df.loc[c]['popularity'] for c in casts]
        top_10_crew_popularity = [crews_df.loc[c]['popularity'] for c in crews]
        top_10_cast_popularity_mean = np.mean(top_10_cast_popularity)
        top_10_crew_popularity_mean = np.mean(top_10_crew_popularity)
    else:
        Directors = pd.read_csv(f"{FILE_DIR}/random_Directors_list.csv").sample(n = 2)['Directors'].tolist()
        Writers = pd.read_csv(f"{FILE_DIR}/random_Writers_list.csv").sample(n = 2)['Writers'].tolist()
        num_of_crew = random.randint(1, 9)
        crews = pd.read_csv(f"{FILE_DIR}/random_crews_list.csv").sample(n = num_of_crew)['crews'].tolist()
        num_of_cast = random.randint(4, 10)
        casts = pd.read_csv(f"{FILE_DIR}/random_casts_list.csv").sample(n = num_of_cast)['casts'].tolist()
        top_10_cast_popularity = [getPopularity(c) for c in casts]
        top_10_crew_popularity = [getPopularity(c) for c in crews]
        top_10_cast_popularity_mean = np.mean(top_10_cast_popularity)
        top_10_crew_popularity_mean = np.mean(top_10_crew_popularity)
    original_language = 'en'
    release_date = date.today().strftime("%Y/%m/%d")
    overview = pd.read_csv(f"{FILE_DIR}/overviews_list.csv").sample(n = 1)['overview'].tolist()[0]
    company_name = pd.read_csv(f"{FILE_DIR}/company_name_list.csv").sample(n = 1)['company_name'].tolist()[0]
    keywords_name = pd.read_csv(f"{FILE_DIR}/keywords_list.csv").sample(n = 2)['keywords_name'].tolist()
    tagline = pd.read_csv(f"{FILE_DIR}/tagline_list.csv").sample(n = 1)['tagline'].tolist()[0]
    homepage = 'None' if random.randint(0, 1) == 1 else pd.read_csv(f"{FILE_DIR}/homepage.csv").sample(n = 1)['homepage'].tolist()[0]
    belongs_to_collection = 'None' if random.randint(0, 1) == 1 else pd.read_csv(f"{FILE_DIR}/btc.csv").sample(n = 1)['belongs_to_collection'].tolist()[0]
    attrs = [num_genres, primaryTitle, genres, originalTitle, isAdult, release_year_int, runtimeMinutes, Directors, Writers, num_of_crew, \
            crews, num_of_cast, casts, original_language, release_date, overview, company_name, keywords_name, top_10_cast_popularity, top_10_crew_popularity, \
            top_10_crew_popularity_mean, top_10_cast_popularity_mean, tagline, homepage, belongs_to_collection]
    attrs_names = ['num_genres', 'primaryTitle', 'genres', 'originalTitle', 'isAdult', 'release_year_int', 'runtimeMinutes', 'Directors', 'Writers', 'num_of_crew', \
        'crews', 'num_of_cast', 'casts', 'original_language', 'release_date', 'overview', 'company_name', 'keywords_name', 'top_10_cast_popularity', 'top_10_crew_popularity', \
        'top_10_crew_popularity_mean', 'top_10_cast_popularity_mean', 'tagline', 'homepage', 'belongs_to_collection']
    input_dict = {}
    for i, k in enumerate(attrs_names):
        input_dict[k] = attrs[i]
    return input_dict

def class_counter(vs, classA, classB):
    cnt_a, cnt_b, cnt_c = 0,0,0
    for v in vs:
        if (v >= classA):
            cnt_a += 1
        elif (v >= classB) & (v < classA):
            cnt_b += 1
        else:
            cnt_c += 1
    return [cnt_a, cnt_b, cnt_c]
def holiday_lists():
    cal = USFederalHolidayCalendar()
    holidays = cal.holidays(start='2021-01-01', end='2021-12-31').to_pydatetime()
    hs = []
    for h in holidays:
        hs.append(h.strftime("%Y/%m/%d"))
    return hs

def top_low(field, name, inputs):
    tops_dir = pd.read_csv(f"{FILE_DIR}/top_{name}_list.csv")
    lows_dir = pd.read_csv(f"{FILE_DIR}/low_{name}_list.csv")
    pd_set_h = set(tops_dir[field].tolist())
    npd_set_low = set(lows_dir[field].tolist())
    l = len(set(inputs[field]) & pd_set_h)
    r = len(set(inputs[field]) & npd_set_low)
    return l,r

def processing_input(inputs):
    CAST_P_A, CAST_P_B, CREW_P_A, CREW_P_B = 0.905193832639673, 0.5270925962298626, 0.6830968447064438, 0.47000362924573563
    inputs['cast_classA'], inputs['cast_classB'], inputs['cast_classC']  = class_counter(inputs['top_10_cast_popularity'], CAST_P_A, CAST_P_B)
    inputs['crew_classA'], inputs['crew_classB'], inputs['crew_classC']  = class_counter(inputs['top_10_crew_popularity'], CREW_P_A, CREW_P_B)
    
    tops_casts = pd.read_csv(f"{FILE_DIR}/tops_casts_list.csv")
    lows_casts = pd.read_csv(f"{FILE_DIR}/lows_casts_list.csv")
    pc_set_h = set(tops_casts['casts'].tolist())
    npc_set_low = set(lows_casts['casts'].tolist())
    inputs['popularCasts'] = len(set(inputs['casts']) & pc_set_h)
    inputs['notPopularCasts'] = len(set(inputs['casts']) & npc_set_low)
    tops_crews = pd.read_csv(f"{FILE_DIR}/tops_crews_list.csv")
    lows_crews= pd.read_csv(f"{FILE_DIR}/lows_crews_list.csv")
    pcr_set_h = set(tops_crews['crews'].tolist())
    npcr_set_low = set(lows_crews['crews'].tolist())
    inputs['popularCrews'] = len(set(inputs['casts']) & pcr_set_h)
    inputs['notPopularCrews'] = len(set(inputs['casts']) & npcr_set_low)
    # print(inputs['popularCasts'], inputs['notPopularCasts'], inputs['popularCrews'], inputs['notPopularCrews'])
    inputs['hasMoreTitles'] = int(inputs['primaryTitle'] == inputs['originalTitle'])
    hs = holiday_lists()
    inputs['isHoliday'] = int(inputs['release_date'] in hs)
    inputs['hasHomepage'] = int(inputs['homepage'] == 'None')
    inputs['hasCollection'] = int(inputs['belongs_to_collection'] == 'None')
    gens = ['Comedy', 'Talk-Show', 'Reality-TV', 'Documentary', 'Science Fiction', 'News', 'Thriller', 'Horror', \
            'Biography', 'Short', 'Drama', 'Music', 'Sci-Fi','Action']
    for g in gens:
        inputs['is'+g] = int(g in inputs['genres'] )
    hdir, ldir = top_low('Directors', 'director',inputs)
    inputs['topDirectors'] = hdir
    inputs['lowDirectors'] = ldir
    hw, lw = top_low('Writers', 'Writers',inputs)
    inputs['topWriters'] = hw
    inputs['lowWriters'] = lw
    langs = ['en', 'es', 'fr']
    for l in langs:
        inputs['is_'+l] = int(inputs['original_language'] == l)
    ks = ['woman director', 'murder', 'based on novel or book']
    for k in ks:
        inputs['is_'+k.replace(' ','_')] = int(k in inputs['keywords_name'])
    inputs['len_overview'] = len(inputs['overview'])
    comps = ['Canal+', 'Warner Bros. Pictures', 'Universal Pictures', 'CNC','CJ Entertainment', \
            'ARTE', 'ZDF', 'Rai Cinema', 'France 2 Cinéma', 'ARTE France Cinéma']
    for c in comps:
        inputs['is_'+c.replace(' ','_')] = int(c in inputs['company_name'])
    inputs['tagline_len'] = len(inputs['tagline'])
    inputs['tag_overview'] = inputs['tagline_len'] / (inputs['len_overview']+1)
    keys_to_drop = ['primaryTitle','genres','originalTitle','Directors','Writers','crews', \
                    'casts', 'original_language', 'release_date', 'overview', 'company_name', \
                    'keywords_name', 'top_10_cast_popularity', 'top_10_crew_popularity', \
                    'tagline', 'homepage', 'belongs_to_collection']
    for k in keys_to_drop:
        if k in inputs: del inputs[k]
    output_order = ['isAdult', 'runtimeMinutes', 'num_of_cast', \
       'top_10_cast_popularity_mean', 'num_of_crew', \
       'top_10_crew_popularity_mean', 'release_year_int', 'cast_classA', \
       'cast_classB', 'cast_classC', 'crew_classA', 'crew_classB', \
       'crew_classC', 'popularCasts', 'notPopularCasts', 'popularCrews', \
       'notPopularCrews', 'hasMoreTitles', 'isHoliday', 'hasHomepage', \
       'hasCollection', 'isComedy', 'isTalk-Show', 'isReality-TV', \
       'isDocumentary', 'isScience Fiction', 'isNews', 'isThriller', \
       'isHorror', 'isBiography', 'isShort', 'isDrama', 'isMusic', 'isSci-Fi', \
       'isAction', 'num_genres', 'topDirectors', 'lowDirectors', 'topWriters', \
       'lowWriters', 'is_en', 'is_es', 'is_fr', 'is_woman_director', \
       'is_murder', 'is_based_on_novel_or_book', 'len_overview', 'is_Canal+', \
       'is_Warner_Bros._Pictures', 'is_Universal_Pictures', 'is_CNC', \
       'is_CJ_Entertainment', 'is_ARTE', 'is_ZDF', 'is_Rai_Cinema', \
       'is_France_2_Cinéma', 'is_ARTE_France_Cinéma', 'tagline_len', 'tag_overview']
    output_dict = {k: inputs[k] for k in output_order}
    # print(output_dict)
    return np.array(list(output_dict.values())).reshape(1, -1)


# inputs = random_input(False)
# x = processing_input(inputs)
# # print(x)
# import pickle
# from sklearn.metrics import r2_score
# loaded_model = pickle.load(open('random_forest_model.pkl', 'rb'))
# y_pred = loaded_model.predict(x)
# print(y_pred)

if __name__ == "__main__":
    # inputs = random_input(True)
    # x = processing_input(inputs)
    # print(x)
    # import pickle
    # from sklearn.metrics import r2_score
    # loaded_model = pickle.load(open('random_forest_model.pkl', 'rb'))
    # y_pred = loaded_model.predict(x)
    # print(y_pred)
    random_list = []
    for _ in range(80):
        random_list.append(random_input(False))
    random_good_list = []
    for _ in range(80):
        random_good_list.append(random_input(True))
    pd.DataFrame.from_dict(random_list).to_csv(f'{FILE_DIR}/random80.csv',encoding='utf-8',index=False)
    pd.DataFrame.from_dict(random_good_list).to_csv(f'{FILE_DIR}/random_good_80.csv',encoding='utf-8',index=False)


