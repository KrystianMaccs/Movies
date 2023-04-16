from django.db.models import Count
from apps.tickets.models import Ticket
from pymongo import MongoClient
from celery import shared_task
from decouple import config



@shared_task
def update_trending_movies():
    client = MongoClient(host=config("MONGO_HOST", cast=str), port=config("MONGO_PORT", cast=int))
    db = client[config("MONGO_NAME")]
    tickets = Ticket.objects.all().annotate(num_tickets=Count('movie__tickets')).order_by('-num_tickets')[:100]
    trending_movies = list(tickets.values())
    db.trending_movies.update_one({'_id': 'trending_movies'}, {'$set': {'movies': trending_movies}}, upsert=True)

