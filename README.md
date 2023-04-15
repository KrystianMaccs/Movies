# Django-Ninja App

This is a Movie API built with Django- Ninja. It makes use of a PostgreSQL Database as well as MongoDB. The API allows query of trending movies from a mongodb database. 


Prerequisites
-------------


To run this application, you will need to have the following installed on your system:

- Docker
- Docker Compose

Installation
------------

Clone the repository to your local machine:

git clone https://github.com/KrystianMaccs/Movies.git
Create a .env file in the root directory of your project and set the required environment variables as listed in the .env.example file. 

Build and run the Docker containers using Docker Compose:

docker-compose up -d --build
Apply the database migrations:

docker-compose exec web python manage.py migrate
Create a superuser (optional):


docker-compose exec web python manage.py createsuperuser


Usage
-----
Once the containers are running, you can access the web application by visiting http://localhost:8000/ in your web browser. You can also visit http://localhost:8000/api/docs to see the different endpoints on the API. In addition, you can access the Django admin panel by visiting http://localhost:8000/admin/.


Troubleshooting
---------------
If you encounter any issues while running the application, try the following:

Check the Docker logs for any error messages:


docker-compose logs -f
Ensure that the required ports (8000, 5432, 6379) are not in use by other applications on your system.

If you make changes to the Dockerfile or docker-compose.yml file, rebuild the containers using:


docker-compose up -d --build

Credits
-------

This application was created by Christian Maximilian(krystianmaccs@gmail.com) and is distributed under the Creative Commons license.

License
