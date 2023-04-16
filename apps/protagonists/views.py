from typing import List
from ninja import Router, Schema
from django.shortcuts import get_object_or_404
from apps.movies.models import Movie
from .models import Protagonist
from .schemas import ProtagonistSchema

router = Router()


@router.post("/protagonists")
def create_protagonist(request, protagonist: ProtagonistSchema):
    protagonist = Protagonist.objects.create(**protagonist.dict())
    return {"id": protagonist.id}

@router.get("/protagonists/{protagonist_id}", response=ProtagonistSchema)
def get_protagonist(request, protagonist_id: int):
    protagonist = get_object_or_404(Protagonist, id=protagonist_id)
    return protagonist

@router.get("/protagonists", response=List[ProtagonistSchema])
def list_protagonists(request):
    protagonists = Protagonist.objects.all()
    return protagonists 

@router.put("/protagonists/{protagonist_id}")
def update_protagonist(request, protagonist_id: int, protagonist: ProtagonistSchema):
    protagonist = get_object_or_404(Protagonist, id=protagonist_id)
    for attr, value in protagonist.dict().items():
        setattr(protagonist, attr, value)
        protagonist.save()
        return {"success": True}

@router.delete("/protagonists/{protagonist_id}")
def delete_protagonist(request, protagonist_id: int):
        protagonist = get_object_or_404(Protagonist, id=protagonist_id)
        protagonist.delete()
        return {"success": True}
