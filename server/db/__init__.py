from server.db.database import Database, transactional
from server.db.models import CategoriesTable, UtcTimestamp, UtcTimestampException, VideosTable
from server.settings import app_settings

db = Database(app_settings.DATABASE_URI)

__all__ = [
    "transactional",
    "VideosTable",
    "CategoriesTable",
    "UtcTimestamp",
    "UtcTimestampException",
    "db",
]
