from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from apps.movies.views import router as movies_router
from apps.tickets.views import router as tickets_router
from apps.ratings.views import router as ratings_router
from apps.users.views import router as users_router
from apps.protagonists.views import router as protagonists_router



api = NinjaAPI()

api.add_router("/movies", movies_router)
api.add_router("/tickets", tickets_router)
api.add_router("/ratings", ratings_router)
api.add_router("/users", users_router)
api.add_router("/protagonists", protagonists_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]

