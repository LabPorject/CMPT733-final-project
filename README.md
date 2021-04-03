# CMPT733-final-project

## Final project for CMPT 733 big data lab

### Current data source:

### MongoDB:

docker-compose version: 1.27.4+
```
cd CMPT733-final-project
```
Edit docker-compose file "bind-mount source" location accordingly
Edit .aws/credentials & configs
```
aws s3 cp s3://data-aoligei/Data-Apr3/Data.zip .
```

```
unzip Data.zip
```
```
pip install pymongo
```
```
docker-compose up -d
```
OPTIONAL: 
```
sudo docker exec -it cmpt733-final-project_mongo_1 bash
```
mongo-express web-front end: http://localhost:8081/

##### interaction with the database has been encapsulated in scripts/query_database.py
see dummy.py as an example

#### Note:
all "\_id" in mongodb collections are all refering to IMDB id.

### Data source:
https://grouplens.org/datasets/movielens/latest/

https://developers.themoviedb.org/3/movies/get-movie-credits