from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from apps.movies.models import Movies
from cinema.utils import get_collection_handle

@receiver(post_save, sender=Movie)
def sync_movie_post_save(sender, instance, **kwargs):
    collection = get_collection_handle(db_handle, 'movies')
    collection.update_one({'_id': instance.id}, {'$set': instance.__dict__}, upsert=True)

@receiver(post_delete, sender=Movie)
def sync_movie_post_delete(sender, instance, **kwargs):
    collection = get_collection_handle(db_handle, 'movies')
    collection.delete_one({'_id': instance.id})

@receiver(pre_save, sender=Movie)
def sync_movie_pre_save(sender, instance, **kwargs):
    if instance.id is None:
        instance.id = uuid.uuid4()
