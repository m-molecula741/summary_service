from uuid import UUID

from fastapi import HTTPException, status
from uuid_extensions import uuid7

from app.db.uow import SqlAlchemyUnitOfWork as UOW
from app.models.teacher import (
    QueryTeachers,
    TeacherCreate,
    TeacherRequest,
    TeachersResponse,
)


class TeacherService:
    @classmethod
    async def create_teacher(cls, uow: UOW, teacher: TeacherRequest) -> UUID:
        async with uow:
            teacher_out, err = await uow.teachers.find_one(full_name=teacher.full_name)
            if err and err != "Data not found":  # noqa: F821
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

            if teacher_out:
                return teacher_out.id

            teacher, err = await uow.teachers.add(
                obj_in=TeacherCreate(**teacher.dict(), id=uuid7())
            )
            if err:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

            return teacher.id

    @classmethod
    async def get_teachers(cls, uow: UOW, query: QueryTeachers):
        async with uow:
            teachers, count, err = await uow.teachers.get_teachers(query=query)
            if err:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=err,
                )

            pages, page_size = TeachersResponse.get_pages(count, query.page_size)

            teachers_resp = TeachersResponse(
                count=count, pages=pages, page_size=page_size, result=teachers
            )

            return teachers_resp
