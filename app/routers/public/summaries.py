from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.models.summary import QuerySummaries, SummariesResponse, SummaryResponse
from app.routers.dependencies import UOWDep
from app.services.summaries_service import SummaryService

router = APIRouter()


@router.get(
    path="/{summary_id}",
    status_code=status.HTTP_200_OK,
    response_model=SummaryResponse,
)
async def get_summary_by_id(summary_id: UUID, uow: UOWDep) -> SummaryResponse:
    """Ручка получения конспекта"""
    summary = await SummaryService.get_summary_by_id(
        uow=uow, summary_id=summary_id, is_public=True
    )

    return SummaryResponse.from_orm(summary)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=SummariesResponse,
)
async def get_summaries(
    uow: UOWDep, query: QuerySummaries = Depends()
) -> SummariesResponse:
    """Ручка получения списка конспектов"""
    summaries_resp = await SummaryService.get_summaries(uow=uow, query=query)

    return summaries_resp
