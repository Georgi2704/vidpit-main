from http import HTTPStatus
from uuid import uuid4

import pytest

from server.db import VideosTable
from server.utils.json import json_dumps


def test_videos_get_multi(video_1, test_client):
    response = test_client.get("/api/videos")

    assert HTTPStatus.OK == response.status_code
    videos = response.json()

    assert 1 == len(videos)


def test_video_by_id(video_1, test_client):
    response = test_client.get(f"/api/videos/{video_1}")

    assert HTTPStatus.OK == response.status_code
    video = response.json()
    assert video["name"] == "Video 1"


def test_video_by_id_404(video_1, test_client):
    response = test_client.get(f"/api/videos/{str(uuid4())}")
    assert HTTPStatus.NOT_FOUND == response.status_code


# def test_video_create(test_client):
#     p_id = uuid4()
#     body = {
#         "video_id": str(p_id),
#         "name": "Video",
#         "description": "Video description",
#     }
#
#     response = test_client.post(
#         "/api/videos/",
#         data=json_dumps(body),
#         headers={"Content_Type": "application/json"},
#     )
#     assert HTTPStatus.NO_CONTENT == response.status_code
#     videos = test_client.get("/api/videos").json()
#     assert 1 == len(videos)


def test_video_delete(video_1, test_client):
    response = test_client.delete(f"/api/videos/{video_1}")
    assert HTTPStatus.NO_CONTENT == response.status_code
    assert len(VideosTable.query.all()) == 0
