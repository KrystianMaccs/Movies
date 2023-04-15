from django.http import Http404
from ninja import Router, Schema
from apps.movies.models import Movie
from .models import Protagonist
from .schemas import ProtagonistSchema

router = Router()


@router.get("/protagonists")
def list_protagonists(request):
    protagonists = Protagonist.objects.all()
    return [ProtagonistSchema.from_orm(p) for p in protagonists]


@router.post("/protagonists", response=ProtagonistSchema)
def create_protagonist(request, protagonist_in: ProtagonistSchema):
    try:
        movie = Movie.objects.get(pk=protagonist_in.movie_id)
    except Movie.DoesNotExist:
        raise Http404("Movie not found")
    protagonist = Protagonist(name=protagonist_in.name, movie=movie)
    protagonist.save()
    return ProtagonistSchema.from_orm(protagonist)


@router.get("/protagonists/{protagonist_id}", response=ProtagonistSchema)
def get_protagonist(request, protagonist_id: int):
    try:
        protagonist = Protagonist.objects.get(pk=protagonist_id)
    except Protagonist.DoesNotExist:
        raise Http404("Protagonist not found")
    return ProtagonistSchema.from_orm(protagonist)


@router.put("/protagonists/{protagonist_id}", response=ProtagonistSchema)
def update_protagonist(request, protagonist_id: int, protagonist_in: ProtagonistSchema):
    try:
        protagonist = Protagonist.objects.get(pk=protagonist_id)
    except Protagonist.DoesNotExist:
        raise Http404("Protagonist not found")
    try:
        movie = Movie.objects.get(pk=protagonist_in.movie_id)
    except Movie.DoesNotExist:
        raise Http404("Movie not found")
    protagonist.name = protagonist_in.name
    protagonist.movie = movie
    protagonist.save()
    return ProtagonistSchema.from_orm(protagonist)


@router.delete("/protagonists/{protagonist_id}")
def delete_protagonist(request, protagonist_id: int):
    try:
        protagonist = Protagonist.objects.get(pk=protagonist_id)
    except Protagonist.DoesNotExist:
        raise Http404("Protagonist not found")
    protagonist.delete()
    return {"success": True}
