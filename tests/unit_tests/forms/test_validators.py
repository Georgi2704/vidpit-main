import pytest
from pydantic import BaseModel, ValidationError

from server.forms.validators import unique_conlist


def test_constrained_list_good():
    class UniqueConListModel(BaseModel):
        v: unique_conlist(int, unique_items=True) = []

    m = UniqueConListModel(v=[1, 2, 3])
    assert m.v == [1, 2, 3]


def test_constrained_list_default():
    class UniqueConListModel(BaseModel):
        v: unique_conlist(int, unique_items=True) = []

    m = UniqueConListModel()
    assert m.v == []
