import query_db_web as qdw
import copy
import json
import ast
import numpy as np
import random_generator as rg
hs = ['2021/01/01', '2021/01/18', '2021/02/15', '2021/05/31', \
            '2021/07/05', '2021/09/06', '2021/10/11', '2021/11/11', '2021/11/25', '2021/12/24', '2021/12/31']

def str_to_list(inputs):
    lists_attr = ['genres', 'Directors', 'Writers',  'crews', 'casts', \
        'keywords_name', 'top_10_cast_popularity', 'top_10_crew_popularity']
    for a in lists_attr:
        print(a)
        inputs[a] = ast.literal_eval(inputs[a])

def top_low(field, inputs):
    tops_dir = qdw.get_maxxu_list(which=f'high_{field}')
    lows_dir = qdw.get_maxxu_list(which=f'low_{field}')
    # print(tops_dir)
    pd_set_h = set(tops_dir)
    npd_set_low = set(lows_dir)
    l = len(set(inputs[field]) & pd_set_h)
    r = len(set(inputs[field]) & npd_set_low)
    return l,r
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

def processing_input(inputs):
    # str_to_list(inputs)
    CAST_P_A, CAST_P_B, CREW_P_A, CREW_P_B = 0.905193832639673, 0.5270925962298626, 0.6830968447064438, 0.47000362924573563
    inputs['cast_classA'], inputs['cast_classB'], inputs['cast_classC']  = class_counter(inputs['top_10_cast_popularity'], CAST_P_A, CAST_P_B)
    inputs['crew_classA'], inputs['crew_classB'], inputs['crew_classC']  = class_counter(inputs['top_10_crew_popularity'], CREW_P_A, CREW_P_B)
    
    tops_casts = qdw.get_maxxu_list(which='high_casts')
    lows_casts = qdw.get_maxxu_list(which='low_casts')
    pc_set_h = set(tops_casts)
    npc_set_low = set(lows_casts)
    inputs['popularCasts'] = len(set(inputs['casts']) & pc_set_h)
    inputs['notPopularCasts'] = len(set(inputs['casts']) & npc_set_low)
    tops_crews = qdw.get_maxxu_list(which='high_crews')
    lows_crews= qdw.get_maxxu_list(which='low_crews')
    pcr_set_h = set(tops_crews)
    npcr_set_low = set(lows_crews)
    inputs['popularCrews'] = len(set(inputs['casts']) & pcr_set_h)
    inputs['notPopularCrews'] = len(set(inputs['casts']) & npcr_set_low)
    # print(inputs['popularCasts'], inputs['notPopularCasts'], inputs['popularCrews'], inputs['notPopularCrews'])
    inputs['hasMoreTitles'] = int(inputs['primaryTitle'] == inputs['originalTitle'])
    inputs['isHoliday'] = int(inputs['release_date'] in hs)
    inputs['hasHomepage'] = int(inputs['homepage'] == 'None')
    inputs['hasCollection'] = int(inputs['belongs_to_collection'] == 'None')
    gens = ['Comedy', 'Talk-Show', 'Reality-TV', 'Documentary', 'Science Fiction', 'News', 'Thriller', 'Horror', \
            'Biography', 'Short', 'Drama', 'Music', 'Sci-Fi','Action']
    for g in gens:
        inputs['is'+g] = int(g in inputs['genres'] )
    hdir, ldir = top_low('Directors',inputs)
    inputs['topDirectors'] = hdir
    inputs['lowDirectors'] = ldir
    hw, lw = top_low('Writers', inputs)
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

def get_lists(req, nums, name):
    cc_prefix = ['f','s','t','fo','fi','six']
    res = []
    for i in range(nums):
        p = req.get(cc_prefix[i]+name)
        if p != '':
            res.append(p)
    return res

def processing_cus_input(req):
    print(req)
    cc_prefix = ['f','s','t','fo','fi','six']
    outs = {}
    print(req.get('isAdult'))
    outs['isAdult'] = int(req.get('isAdult'))
    outs['genres'] = ['None'] if req.get('genres') == 'Genres' else [req.get('genres')]
    outs['num_genres'] = 1
    outs['primaryTitle'],outs['originalTitle'] = req.get('ptitle'), req.get('otitle')
    outs['release_date'], outs['release_year_int'] = req.get('release_date'), int(req.get('release_date').split('-')[0])
    outs['runtimeMinutes'] = float(req.get('runtime'))
    outs['casts'] = get_lists(req, 6, 'cast')
    outs['num_of_cast'] = len(outs['casts'])
    outs['crews'] = get_lists(req, 6, 'crew')
    outs['num_of_crew'] = len(outs['crews'])
    outs['Directors'] = get_lists(req, 3, 'director')
    outs['Writers'] = get_lists(req, 3, 'writer')
    outs['original_language'] = 'en'
    outs['overview'] = req.get('overview')
    outs['company_name'] = []
    outs['homepage'] = 'None' if req.get('homepage') == '' else req.get('homepage')
    outs['tagline'] = req.get('tagline')
    outs['belongs_to_collection'] = 'None' if req.get('collection') == 'Collection' else req.get('collection')
    outs['keywords_name'] = [req.get('keywords')]
    outs['top_10_cast_popularity'] = [rg.getPopularity(c) for c in outs['casts']]
    outs['top_10_crew_popularity'] = [rg.getPopularity(c) for c in outs['crews']]
    outs['top_10_cast_popularity_mean'] = np.mean(outs['top_10_cast_popularity'])
    outs['top_10_crew_popularity_mean'] = np.mean(outs['top_10_crew_popularity'])
    print(outs)
    # processed_outs = processing_input(outs)
    return outs
# content = qdw.low_rating_random_movie()
# x = str_to_list(content)
# print(content)
# x = processing_input(copy.deepcopy(content))
# print(x)
# y_pred = qdw.get_model('rating',Description='Random Forest v2').predict(processing_input(copy.deepcopy(content)))
# content['rating'] = y_pred
# print(y_pred)