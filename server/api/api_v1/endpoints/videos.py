# Copyright 2019-2020 SURF.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import HTTPException
from fastapi.param_functions import Body, Depends
from fastapi.routing import APIRouter
from starlette.responses import Response

from server.api.deps import common_parameters
from server.api.error_handling import raise_status
from server.crud import video_crud
from server.db.models import VideosTable
from server.schemas import Video, VideoCreate, VideoUpdate

router = APIRouter()


@router.get("/", response_model=List[Video])
def get_multi(response: Response, common: dict = Depends(common_parameters)) -> List[Video]:
    videos, header_range = video_crud.get_multi(
        skip=common["skip"],
        limit=common["limit"],
        filter_parameters=common["filter"],
        sort_parameters=common["sort"],
    )
    response.headers["Content-Range"] = header_range
    return videos


@router.get("/{id}", response_model=Video)
def get_by_id(id: UUID) -> VideosTable:
    video = video_crud.get(id)
    if not video:
        raise_status(HTTPStatus.NOT_FOUND, f"Video id {id} not found")
    return video


@router.post("/", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def create(data: VideoCreate = Body(...)) -> None:
    return video_crud.create(obj_in=data)


@router.put("/{video_id}", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def update(*, video_id: UUID, item_in: VideoUpdate) -> None:
    video = video_crud.get(id=video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    video = video_crud.update(
        db_obj=video,
        obj_in=item_in,
    )
    return video


@router.delete("/{video_id}", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def delete(video_id: UUID) -> None:
    return video_crud.delete(id=video_id)
