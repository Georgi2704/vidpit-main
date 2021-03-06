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

from server.schemas.category import Category, CategoryCreate, CategoryUpdate
from server.schemas.msg import Msg
from server.schemas.token import Token, TokenPayload
from server.schemas.user import User, UserCreate, UserUpdate
from server.schemas.video import Video, VideoCreate, VideoUpdate

__all__ = (
    "Category",
    "CategoryCreate",
    "CategoryUpdate",
    "Video",
    "VideoCreate",
    "VideoUpdate",
    "Token",
    "TokenPayload",
    "User",
    "UserCreate",
    "UserUpdate",
    "Msg",
)
