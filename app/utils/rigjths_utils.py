import json

from fastapi import Request


async def get_id_from_request(
    request: Request, query_id_name: str, body_id_name: str
) -> str | None:
    params = request.path_params

    if params:
        return params.get(query_id_name, None)

    body = await request.body()
    if body:
        body = json.loads(body.decode())
        return body.get(body_id_name, None)  # type: ignore

    return None
