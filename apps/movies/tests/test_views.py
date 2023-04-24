import json
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.movies.models import Movie
#from apps import movies





class MovieTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
    @pytest.mark.django_db
    def test_create_movie(self):
        url = reverse('create_protagonist:create_movies')
        data = {'name': 'The Matrix', 'description': 'A movie about the matrix', 'status': 'Running', 'poster': 'image.png', 'start_date': '2020-10-10'}
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Movie.objects.count() == 1
        assert Movie.objects.get().name == 'The Matrix'
        
    @pytest.mark.django_db
    def test_get_all_movies(self):
        url = reverse('movies:list_movies')
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        
    @pytest.mark.django_db
    def test_get_movie_by_id(self):
        movie = Movie.objects.create(name='The Matrix', description='A movie about the matrix', status='Running', poster='image.png', start_date='2020-10-10')
        url = reverse('movies:get_movie', args=[movie.id])
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'The Matrix'
    @pytest.mark.django_db
    def test_update_movie(self):
        movie = Movie.objects.create(name='The Matrix', description='A movie about the matrix', status='Running', poster='image.png', start_date='2020-10-10')
        url = reverse('movies:update_movie', args=[movie.id])        
        data = {'name': 'The Matrix', 'description': 'A movie about the matrix', 'status': 'Running', 'poster': 'image.png', 'start_date': '2020-10-10'}
        response = self.client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        movie.refresh_from_db()
        assert movie.name == 'The Matrix Reloaded'
        assert movie.start_date == '2020-10-10'

    @pytest.mark.django_db
    def test_delete_movie(self):
        movie = Movie.objects.create(name='The Matrix', description='A movie about the matrix', status='Running', poster='image.png', start_date='2020-10-10')
        url = reverse('movies: delete_movie', args=[movie.id])
        response = self.client.delete(url, format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Movie.objects.count() == 0
