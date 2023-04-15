from celery import shared_task
from pymongo import MongoClient
from django.conf import settings
import psycopg2

@shared_task
def replicate_data():
    # Connect to the MongoDB database
    client = MongoClient(settings.DATABASES['nonrel']['CLIENT']['host'], 
                         settings.DATABASES['nonrel']['CLIENT']['port'])
    db = client[settings.DATABASES['nonrel']['NAME']]
    collection = db['mycollection']
    
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=settings.DATABASES['default'][config('NAME')],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT']
    )
    cursor = conn.cursor()