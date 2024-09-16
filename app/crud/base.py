from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound
from typing import Type, TypeVar, Generic, Optional, List
from app.logger import logger


# Generic type of models.
T = TypeVar('T')


class CRUDRepositoryException(Exception):
    """
    Custom Exception for Repository Errors.
    """
    pass


class CRUDRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> Optional[T]:
        try:
            query = select(self.model).where(self.model.sofascore_id == id)
            result = await db.exec(query)
            entity = result.first()

            return entity
        except Exception as exc:
            logger.error(f"Repository: Get Create error: {str(exc)}")
            raise CRUDRepositoryException(
                "AN unexpected error occured."
            )

    async def get_or_error(self, db: AsyncSession, id: int) -> Optional[T]:
        try:
            query = select(self.model).where(self.model.sofascore_id == id)
            result = await db.exec(query)
            entity = result.first()

            if not entity:
                raise NoResultFound(
                    f"No {self.model.__name__} found with ID {id}.")
            return entity
        except NoResultFound as exc:
            logger.error(f"Error fetching {self.model.__name__}: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc)
            )
        except SQLAlchemyError as exc:
            logger.error(f"Database error: {str(exc)}")
            raise CRUDRepositoryException(
                f"Failed to get {self.model.__name__} by ID: {id}"
            )

    async def get_all(self, db: AsyncSession) -> List[T]:
        try:
            query = select(self.model)
            result = await db.exec(query)
            return result.all()
        except SQLAlchemyError as exc:
            logger.error(f"Database error: {str(exc)}")
            raise CRUDRepositoryException(
                f"Failed to fetch all records for {self.model.__name__}")

    async def create(self, db: AsyncSession, entity: T) -> T:
        try:
            db.add(entity)
            await db.commit()
            await db.refresh(entity)
            return entity
        except IntegrityError as exc:
            logger.error(
                f"Integrity error during creation of {self.model.__name__}: {str(exc)}")
            await db.rollback()  # Rollback in case of failure
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Integrity error: entity may already exist.")
        except SQLAlchemyError as exc:
            logger.error(
                f"Database error during creation of {self.model.__name__}: {str(exc)}")
            raise CRUDRepositoryException(
                f"Failed to create {self.model.__name__}")

    async def update(self, db: AsyncSession, entity: T) -> T:
        try:
            db.add(entity)
            await db.commit()
            await db.refresh(entity)
            return entity
        except IntegrityError as exc:
            logger.error(
                f"Integrity error during update of {self.model.__name__}: {str(exc)}")
            await db.rollback()  # Rollback in case of failure
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Integrity error: update failed.")
        except SQLAlchemyError as exc:
            logger.error(
                f"Database error during update of {self.model.__name__}: {str(exc)}")
            raise CRUDRepositoryException(
                f"Failed to update {self.model.__name__}")

    async def delete(self, db: AsyncSession, entity: T) -> None:
        try:
            await db.delete(entity)
            await db.commit()
        except SQLAlchemyError as exc:
            logger.error(
                f"Database error during deletion of {self.model.__name__}: {str(exc)}")
            await db.rollback()  # Rollback in case of failure
            raise CRUDRepositoryException(
                f"Failed to delete {self.model.__name__}")
