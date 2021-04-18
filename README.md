# CMPT733-final-project

## Final project for CMPT 733 big data lab
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
  <li><a href="#cloud-deployment">Cloud deployment</a></li>
    <li><a href="#local-deployment">Local deployment steps (Optional)</a></li>
    <li><a href="#Scripts">Scripts</a></li>
    <li><a href="#team-members">Team Members</a></li>
  </ol>
</details>


## Cloud deployment
##### Go to:  
Web: http://ec2-52-5-131-199.compute-1.amazonaws.com:5000

if you want to checkout our database, MongoDB Express: http://ec2-52-5-131-199.compute-1.amazonaws.com:8081

## Local deployment steps (Optional)
##### prerequisites 
* docker & docker-compose
* sudo apt install unzip

```
# clone our web branch only, this is a simplified branch for demo purpose
git clone -b web --single-branch https://github.com/LabPorject/CMPT733-final-project.git
```
```
cd CMPT733-final-project
```
```
wget https://data-aoligei.s3.amazonaws.com/Data-Apr11/Data.zip
```
use when above link doesn't work or data inside got removed
Backup link: https://drive.google.com/file/d/1NY2rX-nc0IORTHxNFFDzl7ZkQ11kmpmk/view?usp=sharing
```
unzip Data.zip
```
```
sudo docker-compose up -d
```

Web: http://localhost:5000/  
Please allow 3-5 mins to load trained models

MongoDB Express: http://localhost:8081/

## Scripts
#### scripts/query_database.py & web/query_db_web.py
Python interfaces to encapsulate the MQL queries we often use into Python functions
#### dummy.ipynb
A demonstration of how to use above interfaces
#### mongodb_integration/imdb_integration.ipynb
Early stage of the data preparation procedure for IMDB tables
#### mongodb_integration/movielens_integ.ipynb
Early stage of the data preparation procedure for MovieLens tables
#### mongodb_integration/tmdb_api.py & mongodb_integration/create_tmdb.py
TMDB data preparations
#### mongodb_integration/imtm_dbintegration.py
Final data integration to combine all three sources data
#### pred_processing.ipynb
Main script to process movie information data for movie rating predictor model. 
#### pred_lists.zip
All the inputs and data needed for rating prediction and random generator. 
#### similarity.py
Script to calcualte the similarity matrix for each movie.
#### autoencoder_script.py
Autoencoder neural network.
#### models/content_based.ipynb
The neural network for content based recommendation system
#### models/explict-movie-embedding.ipynb
The neural network for explict collaborative filtering recommendation system
#### models/implict_movie_embedding.ipynb
The neural network for implict collaborative filtering recommendation system
#### recommendation.ipynb
Example notebook for recommendation

## Team Members
#### Zhicheng Xu
#### Rong Li
#### Chao Zhang

## Data source:
https://grouplens.org/datasets/movielens/latest/

https://developers.themoviedb.org/3/movies/get-movie-credits

https://datasets.imdbws.com/
