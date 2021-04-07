import pandas as pd
import numpy as np
import datetime
import math

def cast_crew_dist(df, isCast):
    _group = 'casts'
    if not isCast:
        _group = 'crews'
    casts = df
    # casts = df.dropna(subset=[_group,'popularity'])
    casts = casts[[_group,'popularity','imdb_avgRating']]
    _casts = casts.apply(pd.Series.explode).reset_index(drop=True)
    _casts["popularity"] = _casts.popularity.astype(float)
    casts_groups = _casts.groupby(_group).agg('mean')
    return casts_groups

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


def holiday_checker(d,holidays):
    if d == 'null':
        return 0
    ds = d.split('-')
    if len(ds) != 3:
        return 0
    y,m,d = ds
    y,m,d = int(y),int(m),int(d)
    if datetime.datetime(y,m,d) in holidays:
        return 1
    return 0

def cast_crew_avg_rating(xs, isCast,dist):
    _group = 'casts'
    if not isCast:
        _group = 'crews'
    if isinstance(xs,float):
        return 0
#     dist = pd.read_csv(_group+'_dist.csv').reset_index()
#     dist = dist.reset_index().dropna(subset=['imdb_avgRating'])
    cnt = 0
    r = 0.0
    for x in xs:
        xr = dist[dist[_group].str.contains(x)]['imdb_avgRating']
        if not xr.empty:
            r += xr.values[0]
            cnt += 1
    if cnt == 0:
        return 0
    else:
        return r / cnt


def genres_apply(xs, glist):
    _len = len(glist)
    gl = []
    if isinstance(xs,float):
        return [0] * _len
    else:
        for g in glist:
            if g in xs:
                gl.append(1)
            else:
                gl.append(0)
    return gl      


def topRated(field,df,sizes):
    dfe = df.explode(field).groupby(field).agg(mean_rate=('imdb_avgRating','mean'), \
                                                   c_count = (field,'size'))
    dfe = dfe[dfe['c_count'] > 3]
    dfe.dropna(subset=['mean_rate'],inplace=True)
    tops = dfe.sort_values('mean_rate', ascending=False).reset_index()
    lows = dfe.sort_values('mean_rate', ascending=True).reset_index()
    return tops.head(sizes), lows.head(sizes)

def director_writer_top(xs, tops):
    cnt = 0
    if isinstance(xs,float):
        return 0
    else:
        for x in xs:
            if x in tops:
                cnt += 1
    return cnt

def genres_mean_runtimes(xs, df, rmedian):
    sum_runt = 0.0
    if isinstance(xs,float):
        return rmedian
    else:
        for x in xs:
            sum_runt += df.loc[str(x)]['mean_runtimes']
    return sum_runt / len(xs)

if __name__ == '__main__':
    # df = qd.get_combined()
    # casts = df[['casts','top_10_cast_popularity']]
    

    plot(casts_groups['top_10_cast_popularity'])