from enum import Enum


class SortType(str, Enum):
    """Константы по сортировке."""

    asc = "asc"
    desc = "desc"


CONTENT_TYPE_PDF = ["application/pdf"]
MODERATION_ACCESS = "Конспект прошел модерацию"
