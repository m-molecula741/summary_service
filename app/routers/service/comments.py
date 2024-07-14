from fastapi import APIRouter, Depends, status

from app.models.comment import CommentsResponse, QueryComments
from app.models.user import User
from app.routers.dependencies import (
    UOWDep,
    check_is_superuser,
)
from app.services.comments_service import CommentService
from uuid import UUID

router = APIRouter()


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=CommentsResponse,
)
async def get_comments(
    uow: UOWDep,
    query: QueryComments = Depends(),
    user: User = Depends(check_is_superuser),
) -> CommentsResponse:
    """Ручка получения комментариев с жалобами на конспект"""
    comments = await CommentService.get_comments(uow=uow, query=query, is_complain=True)
    return comments


@router.patch(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=bool,
)
async def approve_comment(
    comment_id: UUID,
    uow: UOWDep,
    user: User = Depends(check_is_superuser),
) -> bool:
    """Ручка утверждения комментария"""
    is_upd = await CommentService.approve_comment(uow=uow, comment_id=comment_id)
    return is_upd
