from fastapi import APIRouter, Depends, status

from app.core.base_schemas import ObjSchema
from app.models.university import QueryUniversities, UniversitiesResponse
from app.routers.dependencies import UOWDep
from app.services.universities_service import UniversityService

router = APIRouter()


@router.get(
    path="", status_code=status.HTTP_200_OK, response_model=UniversitiesResponse
)
async def get_universities(
    uow: UOWDep,
    query: QueryUniversities = Depends(),
) -> ObjSchema:
    """Ручка получения университетов"""
    universities = await UniversityService.get_universities(uow=uow, query=query)
    return universities
