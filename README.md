# CMPT733-final-project

## Final project for CMPT 733 big data lab
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
  <li><a href="#On-premise-deployment">On-premise Deployment</a></li>
    <li><a href="#cloud-deployment">Cloud Deployment</a></li>
    <li><a href="#cloud-deployment">Scripts</a></li>
    <li><a href="#team-members">Team Members</a></li>
  </ol>
</details>


## On-premise Deployment

### Prerequisites:
docker-compose version: 1.27.4+
```
pip install pymongo
```
### Usage:

```
cd CMPT733-final-project
```
Edit docker-compose file "bind-mount source" location accordingly <br>
Edit .aws/credentials & configs
```
aws s3 cp s3://data-aoligei/Data-Apr3/Data.zip .
```

```
unzip Data.zip
```

```
docker-compose up -d
```
OPTIONAL: 
```
sudo docker exec -it cmpt733-final-project_mongo_1 bash
```
#### Mongo front-end
http://localhost:8081/

#### Interaction with the database has been encapsulated in scripts/query_database.py
see [dummy.py](/dummy.ipynb) as an example

#### Web front-end
```
http://localhost:5000/
```
## Cloud Deployment

## Scripts
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
#### Data source:
https://grouplens.org/datasets/movielens/latest/

https://developers.themoviedb.org/3/movies/get-movie-credits