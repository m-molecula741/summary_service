from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse

from app.models.summary import (
    SummaryApprovedStatus,
    SummaryChangeStatusRequest,
    SummaryRejectedStatus,
)
from app.models.user import User
from app.routers.dependencies import UOWDep, check_is_superuser
from app.services.summaries_service import SummaryService

router = APIRouter()


@router.patch(
    path="/status/approved",
    status_code=status.HTTP_200_OK,
    response_model=bool,
)
async def set_approved_status(
    summary_in: SummaryChangeStatusRequest,
    uow: UOWDep,
    user: User = Depends(check_is_superuser),
) -> ORJSONResponse:
    """Административная ручка перелкючения в статус approve"""
    is_updated = await SummaryService.change_status(
        uow=uow,
        summary_id=summary_in.id,
        summary_in=SummaryApprovedStatus(
            moderation_comment=summary_in.modearation_comment
        ),
    )
    return ORJSONResponse(content=is_updated, status_code=status.HTTP_200_OK)


@router.patch(
    path="/status/rejected",
    status_code=status.HTTP_200_OK,
    response_model=bool,
)
async def set_rejected_status(
    summary_in: SummaryChangeStatusRequest,
    uow: UOWDep,
    user: User = Depends(check_is_superuser),
) -> ORJSONResponse:
    """Административная ручка перелкючения в статус rejected"""
    is_updated = await SummaryService.change_status(
        uow=uow,
        summary_id=summary_in.id,
        summary_in=SummaryRejectedStatus(
            moderation_comment=summary_in.modearation_comment
        ),
    )
    return ORJSONResponse(content=is_updated, status_code=status.HTTP_200_OK)
