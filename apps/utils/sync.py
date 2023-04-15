from celery import shared_task
from django.apps import apps
from pymongo import MongoClient
from bson import ObjectId
from ninja.errors import HttpError
from decouple import config

MONGO_URI = 'mongodb://{user}:{password}@{host}:{port}/{db}'.format(
    user=config('MONGO_USER'),
    password=config('MONGO_PASSWORD'),
    host=config('MONGO_HOST'),
    port=config('MONGO_PORT'),
    db=config('MONGO_NAME')
)

mongo_client = MongoClient(MONGO_URI)

@shared_task
def sync_db_changes_to_mongo(app_label, model_name, obj_id, operation):
    try:
        model = apps.get_model(app_label=app_label, model_name=model_name)
        mongo_collection = mongo_client[model_name.lower()]

        if operation == 'create':
            obj = model.objects.get(id=obj_id)
            doc = obj.__dict__
            doc['_id'] = ObjectId(str(obj_id))
            del doc['_state']
            mongo_collection.insert_one(doc)

        elif operation == 'update':
            obj = model.objects.get(id=obj_id)
            doc = obj.__dict__
            doc['_id'] = ObjectId(str(obj_id))
            del doc['_state']
            mongo_collection.replace_one({'_id': ObjectId(str(obj_id))}, doc)

        elif operation == 'delete':
            mongo_collection.delete_one({'_id': ObjectId(str(obj_id))})

        else:
            raise HttpError(status_code=400, detail='Invalid operation')

        return "MongoDB sync successful"

    except Exception as e:
        raise HttpError(status_code=500, detail=f"MongoDB sync failed: {str(e)}")
