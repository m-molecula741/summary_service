from uuid import UUID

from fastapi import HTTPException, status
from uuid_extensions import uuid7

from app.core.base_schemas import ObjSchema
from app.db.uow import SqlAlchemyUnitOfWork as UOW
from app.models.enums.status import Status
from app.models.subject import SubjectIsModeratedUpdate
from app.models.summary import (
    QuerySummaries,
    SummariesResponse,
    SummaryCreate,
    SummaryRequest,
    SummaryResponse,
    SummaryShortResponse,
    SummaryUpdate,
    SummaryUpdateRequest,
)
from app.models.teacher import TeacherIsModeratedUpdate


class SummaryService:
    @classmethod
    async def build_summary_status(
        cls, uow: UOW, subject_id: int, teacher_id: UUID
    ) -> Status:
        async with uow:
            subject, err = await uow.subjects.find_one(id=subject_id)
            if err:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

            teacher, err = await uow.teachers.find_one(id=teacher_id)
            if err:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

            if subject.is_moderated and teacher.is_moderated:
                summary_status = Status.approved
            else:
                summary_status = Status.on_moderation

        return summary_status

    @classmethod
    async def create_summary(
        cls, uow: UOW, summary: SummaryRequest, summary_status: Status, user_id: UUID
    ) -> UUID:
        async with uow:
            summary, err = await uow.summaries.add(
                obj_in=SummaryCreate(
                    **summary.dict(), id=uuid7(), status=summary_status, user_id=user_id
                )
            )
            if err:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

        return summary.id

    @classmethod
    async def update_summary(
        cls, uow: UOW, summary: SummaryUpdateRequest, summary_status: Status
    ) -> bool:
        async with uow:
            is_updated, err = await uow.summaries.update(
                id=summary.id,
                obj_in=SummaryUpdate(**summary.dict(), status=summary_status),
            )
            if err:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

        return True

    @classmethod
    async def get_summary_by_id(
        cls, uow: UOW, summary_id: UUID, user_id: UUID | None = None
    ) -> SummaryResponse:
        async with uow:
            summary_in_db, err = await uow.summaries.find_one(id=summary_id)
            if err:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

            await SummaryResponse.check_conspect_access(
                user_id=user_id, summary=summary_in_db
            )

            universtity_in_db, err = await uow.universities.find_one(
                id=summary_in_db.university_id
            )
            if err:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

            subject_in_db, err = await uow.subjects.find_one(
                id=summary_in_db.subject_id
            )
            if err:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

            teacher_in_db, err = await uow.teachers.find_one(
                id=summary_in_db.teacher_id
            )
            if err:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

            lectures, err = await uow.lectures.get_lectures_by_summary_id(
                summary_id=summary_in_db.id
            )
            if err:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

            summary_resp = SummaryResponse(
                id=summary_in_db.id,
                name=summary_in_db.name,
                user_id=summary_in_db.user_id,
                university=universtity_in_db,
                subject=subject_in_db,
                teacher=teacher_in_db,
                status=summary_in_db.status,
                lectures=lectures if lectures else [],
            )

        return summary_resp

    @classmethod
    async def change_status(
        cls, uow: UOW, summary_id: UUID, summary_in: ObjSchema
    ) -> bool:
        async with uow:
            _, err = await uow.summaries.update(id=summary_id, obj_in=summary_in)
            if err:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

            if summary_in.status == Status.approved:  # type: ignore
                summary_in_db, err = await uow.summaries.find_one(id=summary_id)
                if err:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=err
                    )

                _, err = await uow.teachers.update(
                    id=summary_in_db.teacher_id, obj_in=TeacherIsModeratedUpdate()
                )
                if err:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=err
                    )

                _, err = await uow.subjects.update(
                    id=summary_in_db.subject_id, obj_in=SubjectIsModeratedUpdate()
                )
                if err:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=err
                    )

        return True

    @classmethod
    async def get_summaries(
        cls, uow: UOW, query: QuerySummaries, user_id: UUID = None
    ) -> SummariesResponse:
        async with uow:
            summaries, count, err = await uow.summaries.get_summaries(
                query=query, user_id=user_id
            )
            if err:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

            pages, page_size = SummariesResponse.get_pages(count, query.page_size)

            summaries = [
                SummaryShortResponse(
                    id=summary.id, name=summary.name, user_id=summary.user_id
                )
                for summary in summaries
            ]

        summaries_resp = SummariesResponse(
            count=count, pages=pages, page_size=page_size, result=summaries
        )

        return summaries_resp
