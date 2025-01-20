import pytest
from module_utils.utils import load_objs_from_list


def test_load_objs_from_list():
    class Test:
        def __init__(self, data: dict):
            self.data = data

    data = [
        {"status": True, "changes": {"foo": "bar"}},
        {"status": False, "changes": {"baz": "qux"}},
    ]
    objs = load_objs_from_list(data, Test)

    assert len(objs) == 2
    assert objs[0].data["status"] == True
    assert objs[0].data["changes"] == {"foo": "bar"}
    assert objs[1].data["status"] == False
    assert objs[1].data["changes"] == {"baz": "qux"}
