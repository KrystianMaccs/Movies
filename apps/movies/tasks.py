import os
from typing import List
from datetime import datetime, timedelta
import uuid
import bson
from celery import Celery, shared_task
from .models import Movie
from .schema import MovieSchema
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

app = Celery("movies")

mongo_host = os.getenv('MONGO_HOST', '127.0.0.1')
mongo_port = int(os.getenv('MONGO_PORT', '27017'))
mongo_username = os.getenv('MONGO_USERNAME', 'myuser')
mongo_password = os.getenv('MONGO_PASSWORD', 'mypassword')
mongo_db_name = os.getenv('MONGO_DB_NAME', 'admin')

mongo_client = MongoClient(
    host=mongo_host,
    port=mongo_port,
    username=mongo_username,
    password=mongo_password,
    authSource=mongo_db_name,
)

@shared_task
def update_movie_rank():
    upcoming_movies = Movie.objects.filter(status='upcoming')

    for movie in upcoming_movies:
        start_time = datetime.combine(movie.start_date, datetime.min.time())

        if start_time <= datetime.now():
            if movie.status == 'upcoming':
                movie.ranking = 0
            elif movie.status == 'starting':
                movie.ranking = 10
            elif movie.status == 'running':
                movie.ranking = 20
            elif movie.status == 'finished':
                movie.ranking += 10

            movie.save()

    return None

@shared_task
def get_trending_movies() -> List:
    try:
        update_movie_rank.delay() # call update_movie_rank as a dependency
        movie_collection = mongo_client[mongo_db_name]['movies']
        trending_movies = list(movie_collection.find({'status': 'running'}).sort('ranking', -1).limit(10))
        return trending_movies
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))


@shared_task
def sync_movie_to_mongodb(movie_id):
    try:
        movie_collection = mongo_client[mongo_db_name]['movies']
        movie = Movie.objects.get(id=movie_id)

        movie_document = {
            'id': str(movie.id),
            'name': movie.name,
            'protagonists': movie.protagonists,
            'poster': movie.poster.url,
            'start_date': movie.start_date.isoformat(),
            'ranking': movie.ranking
        }

        uuid_binary = bson.Binary(bytes(movie.id.bytes), subtype=bson.binary.UUID_SUBTYPE)
        movie_document['id'] = uuid_binary

        movie_collection.update_one({'id': str(movie.id)}, {'$set': movie_document}, upsert=True)

        return "Movie synced to MongoDB successfully"
    except Exception as e:
        # Handle the exception here
        return "An error occurred while syncing movie to MongoDB: {}".format(str(e))


movie_id = str(Movie.objects.first().id)
app.conf.beat_schedule = {
   'sync-movies-to-mongodb-every-5-minutes': {
       'task': 'movies.tasks.sync_movie_to_mongodb',
       'schedule': 300.0,
       'args': [movie_id]
   },
}
