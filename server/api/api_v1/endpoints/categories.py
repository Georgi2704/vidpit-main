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
from server.crud import category_crud
from server.db.models import CategoriesTable
from server.schemas import Category, CategoryCreate, CategoryUpdate

router = APIRouter()


@router.get("/", response_model=List[Category])
def get_multi(response: Response, common: dict = Depends(common_parameters)) -> List[Category]:
    categorys, header_range = category_crud.get_multi(
        skip=common["skip"],
        limit=common["limit"],
        filter_parameters=common["filter"],
        sort_parameters=common["sort"],
    )
    response.headers["Content-Range"] = header_range
    return categorys


@router.get("/{id}", response_model=Category)
def get_by_id(id: UUID) -> CategoriesTable:
    category = category_crud.get(id)
    if not category:
        raise_status(HTTPStatus.NOT_FOUND, f"Category id {id} not found")
    return category


@router.post("/", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def create(data: CategoryCreate = Body(...)) -> None:
    return category_crud.create(obj_in=data)


@router.put("/{category_id}", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def update(*, category_id: UUID, item_in: CategoryUpdate) -> None:
    category = category_crud.get(id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category = category_crud.update(
        db_obj=category,
        obj_in=item_in,
    )
    return category


@router.delete("/{category_id}", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def delete(category_id: UUID) -> None:
    # Todo: check product first
    return category_crud.delete(id=category_id)
