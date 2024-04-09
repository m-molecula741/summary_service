import io

from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse

from app.routers.dependencies import UOWDep
from app.utils.telegram_utils import get_file, get_file_info

router = APIRouter()


@router.get(path="", status_code=status.HTTP_200_OK)
async def download_pdf_file(uow: UOWDep, file_id: str) -> StreamingResponse:
    """Ручка получения файла"""

    file_info = await get_file_info(file_id=file_id)
    file = await get_file(file_path=file_info.json()["result"]["file_path"])

    return StreamingResponse(
        content=io.BytesIO(file.content), media_type="application/pdf"
    )
