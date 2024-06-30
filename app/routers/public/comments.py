from fastapi import APIRouter, Depends, status

from app.models.comment import CommentsResponse, QueryComments
from app.routers.dependencies import UOWDep
from app.services.comments_service import CommentService
from uuid import UUID

router = APIRouter()


@router.get(
    path="/{summary_id}",
    status_code=status.HTTP_200_OK,
    response_model=CommentsResponse,
)
async def get_comments(
    summary_id: UUID,
    uow: UOWDep,
    query: QueryComments = Depends(),
) -> CommentsResponse:
    """Ручка получения комментариев на конспект"""
    comments = await CommentService.get_comments(
        uow=uow, query=query, summary_id=summary_id
    )
    return comments
