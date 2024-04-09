import json

from fastapi import Request


async def get_id_from_request(request: Request, id_name: str) -> str | None:
    params = request.path_params

    if params:
        return params.get(id_name, None)

    body = await request.body()
    if body:
        body = json.loads(body.decode())
        return body.get(id_name, None)  # type: ignore

    return None
