from fastapi import APIRouter, Depends, status

from app.models.subject import QuerySubjects, SubjectsResponse
from app.routers.dependencies import UOWDep
from app.services.subjects_service import SubjectService

router = APIRouter()


@router.get(path="", status_code=status.HTTP_200_OK, response_model=SubjectsResponse)
async def get_subjects(
    uow: UOWDep,
    query: QuerySubjects = Depends(),
) -> SubjectsResponse:
    """Ручка получения учебных дисциплин"""
    subjects = await SubjectService.get_subjects(uow=uow, query=query)
    return subjects
