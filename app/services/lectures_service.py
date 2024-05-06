from uuid import UUID

from fastapi import HTTPException, status
from uuid_extensions import uuid7

from app.db.uow import SqlAlchemyUnitOfWork as UOW
from app.models.lecture import (
    LectureCreate,
    LectureCreateRequest,
    LectureUpdate,
    LectureUpdateRequest,
)


class LectureService:
    @classmethod
    async def add_lecture(
        cls, uow: UOW, lecture: LectureCreateRequest, user_id: UUID
    ) -> UUID:
        async with uow:
            summary, err = await uow.summaries.find_one(id=lecture.summary_id)
            if err:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=err,
                )

            if summary.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="No rights"
                )

            lecture_in_db, err = await uow.lectures.add(
                obj_in=LectureCreate(
                    **lecture.dict(),
                    id=uuid7(),
                )
            )
            if err:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=err,
                )

        return lecture_in_db.id

    @classmethod
    async def update_lecture(cls, uow: UOW, lecture: LectureUpdateRequest):
        async with uow:
            is_updated, err = await uow.lectures.update(
                id=lecture.id, obj_in=LectureUpdate(**lecture.dict())
            )
            if err:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=err,
                )

            return is_updated

    @classmethod
    async def delete_lecture(cls, uow: UOW, lecture_id: UUID):
        async with uow:
            is_deleted, err = await uow.lectures.delete(id=lecture_id)
            if err:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=err,
                )

        return is_deleted
