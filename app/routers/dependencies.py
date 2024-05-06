from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from jose import jwt

from app.core.config import config
from app.db.uow import SqlAlchemyUnitOfWork as UOW
from app.models.user import AuthSchema, User
from app.utils.rigjths_utils import get_id_from_request
from app.utils.user_utils import OAuth2PasswordBearerWithCookie

oauth2_scheme = OAuth2PasswordBearerWithCookie(token_url="/login")

# получение объекта uow
UOWDep = Annotated[UOW, Depends(UOW)]


async def get_current_user(token: AuthSchema = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(
            token.credentials, config.secret_key, algorithms=[config.algorithm]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    return User(
        id=UUID(user_id),
        nickname=payload.get("nickname"),
        email=payload.get("email"),
        is_superuser=payload.get("is_superuser"),
    )


async def check_is_superuser(
    active_user: User = Depends(get_current_user),
) -> None:

    if not active_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа. Необходимо быть администратором",
        )

    return None


async def check_access_summary(
    request: Request, uow: UOWDep, user: User = Depends(get_current_user)
) -> None:
    summary_id = await get_id_from_request(
        request=request, query_id_name="summary_id", body_id_name="id"
    )
    summary_in_db, err = await uow.summaries.find_one(id=summary_id)
    if err:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No rights")

    if summary_in_db.user_id != user.id:  # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No rights")

    return None


async def check_access_lecture(
    request: Request, uow: UOWDep, user: User = Depends(get_current_user)
) -> None:
    lecture_id = await get_id_from_request(
        request=request, query_id_name="lecture_id", body_id_name="id"
    )
    lecture, err = await uow.lectures.find_one(id=lecture_id)
    if err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

    summary_in_db, err = await uow.summaries.find_one(id=lecture.summary_id)
    if err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

    if summary_in_db.user_id != user.id:  # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No rights")

    return None
