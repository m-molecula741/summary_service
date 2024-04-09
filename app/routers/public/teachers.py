from fastapi import APIRouter, Depends, status

from app.models.teacher import QueryTeachers, TeachersResponse
from app.routers.dependencies import UOWDep
from app.services.teachers_service import TeacherService

router = APIRouter()


@router.get(path="", status_code=status.HTTP_200_OK, response_model=TeachersResponse)
async def get_teachers(
    uow: UOWDep,
    query: QueryTeachers = Depends(),
) -> TeachersResponse:
    """Ручка получения преподавателей"""
    teachers = await TeacherService.get_teachers(uow=uow, query=query)
    return teachers
