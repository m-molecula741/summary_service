from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse

from app.models.teacher import TeacherRequest
from app.models.user import User
from app.routers.dependencies import UOWDep, get_current_user
from app.services.teachers_service import TeacherService

router = APIRouter()


@router.post(path="", status_code=status.HTTP_201_CREATED, response_model=UUID)
async def create_teacher(
    teacher: TeacherRequest, uow: UOWDep, _: User = Depends(get_current_user)
) -> ORJSONResponse:
    """Ручка создания преподавателя"""
    teacher_id = await TeacherService.create_teacher(uow=uow, teacher=teacher)
    return ORJSONResponse(content=teacher_id, status_code=status.HTTP_201_CREATED)
