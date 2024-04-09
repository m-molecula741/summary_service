from fastapi import File, HTTPException, status

from app.db.uow import SqlAlchemyUnitOfWork as UOW
from app.models.university import QueryUniversities, UniversitiesResponse, UniversityIn


class UniversityService:
    @classmethod
    async def add_universities(cls, uow: UOW, universities: list[UniversityIn]) -> int:
        async with uow:
            universities_ids_db, err = await uow.universities.get_universities_ids()
            if err:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

            added_ids = set(university.id for university in universities) - set(
                universities_ids_db  # type: ignore
            )
            universities_to_add = [
                university for university in universities if university.id in added_ids
            ]

            new_universities, err = await uow.universities.bulk_add(
                obj_ins=universities_to_add  # type: ignore
            )
            if err:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

        return len(added_ids)

    @classmethod
    async def read_csv(cls, file: File) -> list[UniversityIn]:
        if file.content_type != "text/csv":
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")

        contents = await file.read()
        universities = await UniversityIn.from_csv(contents)
        return universities

    @classmethod
    async def get_universities(cls, uow: UOW, query: QueryUniversities):
        async with uow:
            universities, count, err = await uow.universities.get_universities(
                query=query
            )
            if err:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=err,
                )

            pages, page_size = UniversitiesResponse.get_pages(count, query.page_size)

            universities_resp = UniversitiesResponse(
                count=count, pages=pages, page_size=page_size, result=universities
            )

            return universities_resp
