from fastapi import APIRouter, Depends, HTTPException, status

from app.models.comment import CommentComplainRequest, CommentCreateRequest
from app.models.user import User
from app.routers.dependencies import UOWDep, check_access_comment, get_current_user
from app.services.comments_service import CommentService
from app.services.summaries_service import SummaryService
from uuid import UUID

router = APIRouter()


@router.post(path="", status_code=status.HTTP_201_CREATED, response_model=UUID)
async def add_comment(
    comment_in: CommentCreateRequest,
    uow: UOWDep,
    user: User = Depends(get_current_user),
) -> UUID:
    """Ручка добавления коммента к конспекту"""
    is_approved = await SummaryService.is_approved(
        uow=uow, summary_id=comment_in.summary_id
    )
    if not is_approved:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Конспект является приватным",
        )

    comment_id = await CommentService.add_comment(
        uow=uow, comment_in=comment_in, user_id=user.id
    )
    return comment_id


@router.delete(
    path="/{comment_id}", status_code=status.HTTP_201_CREATED, response_model=UUID
)
async def delete_comment(
    comment_id: UUID,
    uow: UOWDep,
    _=Depends(check_access_comment),
) -> UUID:
    """Ручка удаления коммента"""
    comment_id = await CommentService.delete_comment(uow=uow, comment_id=comment_id)
    return comment_id


@router.patch(
    path="/complain", status_code=status.HTTP_201_CREATED, response_model=bool
)
async def complain_on_comment(
    comment_info: CommentComplainRequest,
    uow: UOWDep,
    user: User = Depends(get_current_user),
) -> bool:
    """Пожаловаться на комментарий"""
    is_upd = await CommentService.complain(uow=uow, comment_info=comment_info)
    return is_upd
