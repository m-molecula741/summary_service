from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse

from app.models.subject import SubjectBase
from app.models.user import User
from app.routers.dependencies import UOWDep, get_current_user
from app.services.subjects_service import SubjectService

router = APIRouter()


@router.post(path="", status_code=status.HTTP_201_CREATED, response_model=int)
async def create_subject(
    subject: SubjectBase, uow: UOWDep, _: User = Depends(get_current_user)
) -> ORJSONResponse:
    """Ручка создания учебной дисциплины"""
    subject_id = await SubjectService.add_subject(uow=uow, subject=subject)
    return ORJSONResponse(content=subject_id, status_code=status.HTTP_201_CREATED)
