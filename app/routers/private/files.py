from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.consts import CONTENT_TYPE_PDF
from app.models.file import FileInfoResponse
from app.models.user import User
from app.routers.dependencies import UOWDep, get_current_user
from app.utils.telegram_utils import save_file
from app.core.config import config

router = APIRouter()


@router.post(
    path="", status_code=status.HTTP_201_CREATED, response_model=FileInfoResponse
)
async def upload_pdf_file(
    uow: UOWDep, file: UploadFile = File(...), _: User = Depends(get_current_user)
) -> FileInfoResponse:
    """Ручка сохранения файла"""
    if file.content_type not in CONTENT_TYPE_PDF:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pdf files are allowed",
        )

    response = await save_file(file=file)
    file_id = response.json()["result"]["document"]["file_id"]

    file_info_resp = FileInfoResponse(
        id=file_id,
        name=response.json()["result"]["document"]["file_name"],
        file_url=f"https://{config.domain}{config.public_prefix}/files?file_id={file_id}",
    )

    return file_info_resp
