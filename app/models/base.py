from datetime import datetime
from sqlmodel import Field, SQLModel
from uuid import UUID
from uuid_extensions import uuid7


class IdMixin(SQLModel):
    id: UUID = Field(
        default_factory=uuid7,
        primary_key=True,
        index=True,
        nullable=False,
    )


class TimestampMixin(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now,
                                 nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.now, sa_column_kwargs={
            'onupdate': datetime.now,
        }
    )


class DeleteResponse(SQLModel):
    deleted: int
