from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse

from app.models.lecture import LectureCreateRequest, LectureUpdateRequest
from app.models.user import User
from app.routers.dependencies import (
    UOWDep,
    check_access_lecture,
    check_access_lecture_for_add,
)
from app.services.lectures_service import LectureService

router = APIRouter()


@router.post(path="", status_code=status.HTTP_201_CREATED, response_model=UUID)
async def create_lecture(
    lecture: LectureCreateRequest,
    uow: UOWDep,
    user: User = Depends(check_access_lecture_for_add),
) -> ORJSONResponse:
    """Ручка создания лекции"""
    lecture_id = await LectureService.add_lecture(uow=uow, lecture=lecture)
    return ORJSONResponse(content=lecture_id, status_code=status.HTTP_201_CREATED)


@router.patch(path="", status_code=status.HTTP_200_OK, response_model=bool)
async def update_lecture(
    lecture: LectureUpdateRequest, uow: UOWDep, _=Depends(check_access_lecture)
) -> ORJSONResponse:
    """Ручка обновления лекции"""
    is_updated = await LectureService.update_lecture(uow=uow, lecture=lecture)
    return ORJSONResponse(content=is_updated, status_code=status.HTTP_200_OK)


@router.delete(
    path="/{lecture_id}", status_code=status.HTTP_200_OK, response_model=bool
)
async def delete_lecture(
    lecture_id: UUID, uow: UOWDep, _=Depends(check_access_lecture)
) -> ORJSONResponse:
    """Ручка удаления лекции"""
    is_deleted = await LectureService.delete_lecture(uow=uow, lecture_id=lecture_id)
    return ORJSONResponse(content=is_deleted, status_code=status.HTTP_200_OK)
