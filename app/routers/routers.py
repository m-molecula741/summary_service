from fastapi import APIRouter

from app.routers.private import (
    files as private_files,
    lectures as private_lectures,
    subjects as private_subjects,
    summaries as private_summaries,
    teachers as private_teachers,
    comments as private_comments,
)
from app.routers.public import (
    files as public_files,
    subjects as public_subjects,
    summaries as public_summaries,
    teachers as public_teachers,
    uviversities as public_universities,
    comments as public_comments,
)
from app.routers.service import (
    summaries as service_summaries,
    universities as service_universities,
    comments as service_comments,
)

router_public = APIRouter()
router_public.include_router(
    public_universities.router,
    tags=["Public universities routers"],
    prefix="/universities",
)
router_public.include_router(
    public_subjects.router, tags=["Public subjects routers"], prefix="/subjects"
)
router_public.include_router(
    public_teachers.router, tags=["Public teachers routers"], prefix="/teachers"
)
router_public.include_router(
    public_summaries.router, tags=["Public summaries routers"], prefix="/summaries"
)
router_public.include_router(
    public_files.router, tags=["Public files routers"], prefix="/files"
)
router_public.include_router(
    public_comments.router, tags=["Public comments routers"], prefix="/comments"
)

router_private = APIRouter()
router_private.include_router(
    private_subjects.router, tags=["Private subjects routers"], prefix="/subjects"
)
router_private.include_router(
    private_teachers.router,
    tags=["Private teachers routers"],
    prefix="/teachers",
)
router_private.include_router(
    private_summaries.router,
    tags=["Private summaries routers"],
    prefix="/summaries",
)
router_private.include_router(
    private_lectures.router,
    tags=["Private lectures routers"],
    prefix="/lectures",
)
router_private.include_router(
    private_files.router,
    tags=["Private files routers"],
    prefix="/files",
)
router_private.include_router(
    private_comments.router,
    tags=["Private comments routers"],
    prefix="/comments",
)

router_service = APIRouter()
router_service.include_router(
    service_summaries.router, tags=["Admin summaries routers"], prefix="/summaries"
)
router_service.include_router(
    service_universities.router,
    tags=["Admin universities routers"],
    prefix="/universities",
)
router_service.include_router(
    service_comments.router, tags=["Admin comments routers"], prefix="/summaries"
)
