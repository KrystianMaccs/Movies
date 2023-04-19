import logging
import random
from faker import Faker
from core.models.postgres_models import Post
from celery import shared_task


@shared_task
def create_random_posts():
    fake = Faker()
    number_of_posts = random.randint(5, 100)
    for i in range(number_of_posts):
        try:
            if i % 5 == 0:
                title = None
            else: 
                title = fake.sentence()
            description = fake.text()
            Post.objects.create(
                title = title,
                description = description,
            )
        except Exception as exc:
            logger.error("The post number %s failed due to the %s", i, exc)