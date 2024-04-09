from enum import Enum


class Status(str, Enum):
    rejected = "rejected"
    on_moderation = "on_moderation"
    approved = "approved"

    def __str__(self) -> str:
        """Строковое представление"""
        return self.value
