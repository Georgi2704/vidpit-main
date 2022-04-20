from server.crud.base import CRUDBase
from server.db.models import CategoriesTable
from server.schemas.category import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[CategoriesTable, CategoryCreate, CategoryUpdate]):
    pass


category_crud = CRUDCategory(CategoriesTable)
