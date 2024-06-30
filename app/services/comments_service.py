from fastapi import HTTPException, status
from uuid import UUID
from uuid_extensions import uuid7

from app.db.uow import SqlAlchemyUnitOfWork as UOW
from app.models.comment import (
    CommentApprove,
    CommentComplain,
    CommentComplainRequest,
    CommentCreateRequest,
    CommentCreate,
    CommentsResponse,
    QueryComments,
)


class CommentService:
    @classmethod
    async def add_comment(
        cls, uow: UOW, comment_in: CommentCreateRequest, user_id: UUID
    ) -> UUID:
        async with uow:
            comment, err = await uow.comments.add(
                obj_in=CommentCreate(
                    id=uuid7(),
                    **comment_in.dict(),
                    user_id=user_id,
                )
            )
            if err:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

        return comment.id

    @classmethod
    async def delete_comment(cls, uow: UOW, comment_id: UUID) -> bool:
        async with uow:
            is_deleted, err = await uow.comments.delete(id=comment_id)
            if err:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

            return is_deleted

    @classmethod
    async def get_comments(
        cls, uow: UOW, query: QueryComments, summary_id: UUID, is_complain: bool = False
    ) -> CommentsResponse:
        async with uow:
            comments, count, err = await uow.comments.get_comments(
                query=query, summary_id=summary_id, is_complain=is_complain
            )
            if err:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=err,
                )

            pages, page_size = CommentsResponse.get_pages(count, query.page_size)

            comments_resp = CommentsResponse(
                count=count, pages=pages, page_size=page_size, result=comments
            )

        return comments_resp

    @classmethod
    async def complain(cls, uow: UOW, comment_info: CommentComplainRequest) -> bool:
        async with uow:
            comment_db, err = await uow.comments.find_one(id=comment_info.comment_id)
            if err:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=err,
                )

            if comment_db.is_moderated:
                raise HTTPException(
                    status_code=status.HTTP_423_LOCKED,
                    detail="Данный комментарий уже проверен и не нарушает никаких правил",
                )

            is_updated, err = await uow.comments.update(
                id=comment_info.comment_id, obj_in=CommentComplain()
            )
            if err:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=err,
                )

        return is_updated

    @classmethod
    async def approve_comment(cls, uow: UOW, comment_id: UUID) -> bool:
        async with uow:
            is_upd, err = await uow.comments.update(
                id=comment_id, obj_in=CommentApprove()
            )
            if err:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=err,
                )

            return is_upd
