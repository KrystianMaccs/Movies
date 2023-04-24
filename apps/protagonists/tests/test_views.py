import json
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.protagonists.models import Protagonist





class MovieTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
    @pytest.mark.django_db
    def test_create_protagonist(self):
        url = reverse('create_protagonist:create_protagonist')
        data = {'name': 'Neo', 'movie': 'The Matrix'}
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Protagonist.objects.count() == 1
        assert Protagonist.objects.get().name == 'Neo'
        
    @pytest.mark.django_db
    def test_get_all_protagonists(self):
        url = reverse('movies:list_protagonists')
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        
    @pytest.mark.django_db
    def test_get_protagonist_by_id(self):
        protagonist = Protagonist.objects.create(name='Neo', movie='The Matrix')
        url = reverse('movies:get_protagonist', args=[movie.id])
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Neo'
    @pytest.mark.django_db
    def test_update_protagonist(self):
        protagonist = Protagonist.objects.create(name='Neo', movie='The Matrix')
        url = reverse('movies:update_protagonist', args=[movie.id])        
        data = {'name': 'Neo', 'movie': 'The Matrix'}
        response = self.client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        movie.refresh_from_db()
        assert protagonist.name == 'Neo'
        assert Protagonist.movie == 'The Matrix'

    @pytest.mark.django_db
    def test_delete_protagonist(self):
        protagonist = Protagonist.objects.create(name='Neo', movie='The Matrix')
        url = reverse('movies: delete_protagonist', args=[movie.id])
        response = self.client.delete(url, format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Movie.objects.count() == 0
