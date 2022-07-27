from typing import Optional

from sqlalchemy import desc
from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO, T
from project.models import Genre, Director, Movie, User


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all_order_by(self, page: Optional[int] = None, status=None) -> list[T]:
        stmt = self._db_session.query(self.__model__)
        if status:
            stmt = stmt.order_by(desc(self.__model__.year))
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()


class UsersDAO(BaseDAO[User]):
    __model__ = User
