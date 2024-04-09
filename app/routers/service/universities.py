from fastapi import APIRouter, Depends, File, UploadFile, status

from app.core.base_schemas import ObjSchema
from app.models.university import UniversitiesAddedResponse
from app.models.user import User
from app.routers.dependencies import UOWDep, check_is_superuser
from app.services.universities_service import UniversityService

router = APIRouter()


@router.post(
    path="/upload",
    status_code=status.HTTP_201_CREATED,
    response_model=UniversitiesAddedResponse,
)
async def upload(
    uow: UOWDep, file: UploadFile = File(...), user: User = Depends(check_is_superuser)
) -> ObjSchema:
    """Ручка загрузки справочника университетов"""
    universities = await UniversityService.read_csv(file=file)
    count_added_universities = await UniversityService.add_universities(
        uow=uow, universities=universities
    )
    return UniversitiesAddedResponse(count_added_universities=count_added_universities)
