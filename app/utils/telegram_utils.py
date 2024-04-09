import httpx
from fastapi import UploadFile

from app.core.config import config


async def save_file(file: UploadFile):
    async with httpx.AsyncClient() as client:
        form_data = {
            "chat_id": (None, config.chat_id),
            "document": (file.filename, file.file, file.content_type),
        }

        response = await client.post(
            f"{config.tg_base_url}/sendDocument", files=form_data  # type: ignore
        )

    return response


async def get_file_info(file_id: str):
    async with httpx.AsyncClient() as client:
        form_data = {"file_id": file_id}

        response = await client.get(f"{config.tg_base_url}/getFile", params=form_data)

    return response


async def get_file(file_path: str):
    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"{config.tg_domain}/file/bot{config.bot_token}/{str(file_path)}"
        )

    return response
