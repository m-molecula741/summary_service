from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse

from app.models.summary import (
    QuerySummaries,
    SummariesResponse,
    SummaryRequest,
    SummaryResponse,
    SummaryUpdateRequest,
)
from app.models.user import User
from app.routers.dependencies import UOWDep, check_access_summary, get_current_user
from app.services.summaries_service import SummaryService

router = APIRouter()


@router.post(path="", status_code=status.HTTP_201_CREATED, response_model=UUID)
async def create_summary(
    summary: SummaryRequest, uow: UOWDep, user: User = Depends(get_current_user)
) -> ORJSONResponse:
    """Ручка создания конспекта"""
    summary_status = await SummaryService.build_summary_status(
        uow=uow, subject_id=summary.subject_id, teacher_id=summary.teacher_id
    )

    summary_id = await SummaryService.create_summary(
        uow=uow, summary=summary, summary_status=summary_status, user_id=user.id
    )
    return ORJSONResponse(content=summary_id, status_code=status.HTTP_201_CREATED)


@router.patch(path="", status_code=status.HTTP_200_OK, response_model=bool)
async def update_summary(
    summary: SummaryUpdateRequest, uow: UOWDep, user: User = Depends(get_current_user)
) -> ORJSONResponse:
    """Ручка обновления конспекта"""
    async with uow:
        summary_in_db, err = await uow.summaries.find_one(id=summary.id)
        if err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

    if summary_in_db.user_id != user.id:  # type: ignore
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Нет прав")

    summary_status = await SummaryService.build_summary_status(
        uow=uow,
        subject_id=summary.subject_id
        if summary.subject_id
        else summary_in_db.subject_id,  # type: ignore
        teacher_id=summary.teacher_id  # type: ignore
        if summary.teacher_id
        else summary_in_db.teacher_id,
    )

    is_updated = await SummaryService.update_summary(
        uow=uow, summary=summary, summary_status=summary_status
    )
    return ORJSONResponse(content=is_updated, status_code=status.HTTP_200_OK)


@router.get(
    path="/{summary_id}",
    status_code=status.HTTP_200_OK,
    response_model=SummaryResponse,
)
async def get_private_summary_by_id(
    summary_id: UUID, uow: UOWDep, _=Depends(check_access_summary)
) -> SummaryResponse:
    """Ручка получения конспекта"""
    summary = await SummaryService.get_summary_by_id(uow=uow, summary_id=summary_id)

    return SummaryResponse.from_orm(summary)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=SummariesResponse,
)
async def get_my_summaries(
    uow: UOWDep,
    query: QuerySummaries = Depends(),
    user: User = Depends(get_current_user),
) -> SummariesResponse:
    """Ручка получения списка конспектов юзера"""
    summaries_resp = await SummaryService.get_summaries(
        uow=uow, query=query, user_id=user.id
    )

    return summaries_resp
