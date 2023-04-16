import json
from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from pymongo import MongoClient
from decouple import config


class UtilsConfig(AppConfig):
    name = 'apps.utils'

    def ready(self):
        for model in self.get_models():
            @receiver(post_save, sender=model)
            def save_to_mongodb_signal(sender, instance, **kwargs):
                client = MongoClient(host=config("MONGO_HOST", cast=str), port=config("MONGO_PORT", cast=int))
                db = client[config("MONGO_NAME")]

                # Save the model instance to MongoDB
                mongo_collection_name = 'my_collection'
                mongo_collection = db[mongo_collection_name]
                mongo_object = json.loads(instance.to_json())
                mongo_collection.replace_one({'_id': mongo_object['_id']}, mongo_object, upsert=True)

            @receiver(post_save, sender=model)
            def update_to_mongodb_signal(sender, instance, **kwargs):
                # Connect to MongoDB using pymongo
                client = MongoClient(host=config("MONGO_HOST", cast=str), port=config("MONGO_PORT", cast=int))
                db = client[config("MONGO_NAME")]

                # Update the model instance to MongoDB
                mongo_collection_name = 'my_collection'
                mongo_collection = db[mongo_collection_name]
                mongo_object = json.loads(instance.to_json())
                mongo_collection.update_one({'_id': mongo_object['_id']}, {'$set': mongo_object}, upsert=True)

            @receiver(post_delete, sender=model)
            def pre_delete_from_mongodb_signal(sender, instance, **kwargs):
                # Connect to MongoDB using pymongo
                client = MongoClient(host=config("MONGO_HOST", cast=str), port=config("MONGO_PORT", cast=int))
                db = client[config("MONGO_NAME")]

                # Delete the model instance from MongoDB
                mongo_collection_name = 'my_collection'
                mongo_collection = db[mongo_collection_name]
                mongo_object = json.loads(instance.to_json())
                mongo_collection.delete_one({'_id': mongo_object['_id']})
