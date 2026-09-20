import logging
from typing import Generic, Optional, Tuple, Type, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

logger = logging.getLogger("gcft_api.services.base")

ModelT = TypeVar("ModelT")


class BaseService(Generic[ModelT]):
    """Shared DB helpers so list/get-by-id/count behave identically everywhere."""

    def __init__(self, db: Session, settings=None):
        self.db = db
        self.settings = settings

    def paginate(self, base_query, *, skip: int = 0, limit: int = 20) -> Tuple[list, int]:
        """Execute a select query with offset/limit and return (items, total)."""
        count_query = select(func.count()).select_from(base_query.subquery())
        total = self.db.scalar(count_query) or 0
        items = list(self.db.scalars(base_query.offset(skip).limit(limit)).all())
        return items, total

    def get_by_id(self, model: Type[ModelT], obj_id: int) -> Optional[ModelT]:
        """Fetch a single row by primary key."""
        return self.db.get(model, obj_id)
