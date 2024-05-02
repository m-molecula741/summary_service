from fastapi import HTTPException, status

from app.db.uow import SqlAlchemyUnitOfWork as UOW
from app.models.subject import (
    QuerySubjects,
    SubjectBase,
    SubjectCreate,
    SubjectsResponse,
)


class SubjectService:
    @classmethod
    async def add_subject(cls, uow: UOW, subject: SubjectBase) -> int:
        async with uow:
            subject_out, err = await uow.subjects.find_one(name=subject.name)
            if err and err != "Data not found":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

            if subject_out:
                return subject_out.id

            subject, err = await uow.subjects.add(
                obj_in=SubjectCreate(name=subject.name)
            )
            if err:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

        return subject.id

    @classmethod
    async def get_subjects(cls, uow: UOW, query: QuerySubjects) -> SubjectsResponse:
        async with uow:
            subjects, count, err = await uow.subjects.get_subjects(query=query)
            if err:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=err,
                )

            pages, page_size = SubjectsResponse.get_pages(count, query.page_size)

            subjects_resp = SubjectsResponse(
                count=count, pages=pages, page_size=page_size, result=subjects
            )

            return subjects_resp
