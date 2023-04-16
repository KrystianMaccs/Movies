from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count
from apps.tickets.models import Ticket
from pymongo import MongoClient

@receiver(post_save, sender=Ticket)
def update_trending_movies(sender, **kwargs):
    client = MongoClient(host=config("MONGO_HOST", cast=str), port=config("MONGO_PORT", cast=int))
    db = client[config("MONGO_NAME")]
    tickets = Ticket.objects.all().annotate(num_tickets=Count('movie__tickets')).order_by('-num_tickets')[:100]
    trending_movies = list(tickets.values())
    db.trending_movies.update_one({'_id': 'trending_movies'}, {'$set': {'movies': trending_movies}}, upsert=True)
