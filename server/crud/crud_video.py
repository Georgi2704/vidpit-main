from server.crud.base import CRUDBase
from server.db.models import VideosTable
from server.schemas.video import VideoCreate, VideoUpdate


class CRUDVideo(CRUDBase[VideosTable, VideoCreate, VideoUpdate]):
    pass


video_crud = CRUDVideo(VideosTable)
