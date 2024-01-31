import pytest
from json_decorator import json_method, json_class

SampleJsonRegistry = []

@json_class(SampleJsonRegistry)
class SampleJson:
    @json_method(registry=SampleJsonRegistry)
    def a_string(self):
        return "test"

    @json_method(registry=SampleJsonRegistry)
    def a_digit(self):
        return 10

    @json_method(registry=SampleJsonRegistry)
    def a_list(self):
        return [1,2,3]

    @json_method(registry=SampleJsonRegistry)
    def a_dict(self):
        return {'one': 1, 'two': 2}

@pytest.fixture
def json_object():
    return SampleJson()

class TestDecorator:
    def test_string(self, json_object):
        assert "\"test\"" == json_object.a_string()

    def test_digit(self, json_object):
        assert "10" == json_object.a_digit()

    def test_list(self, json_object):
        assert "[1,2,3]" == json_object.a_list()

    def test_dict(self, json_object):
        assert "{\n\"one\": 1,\n\"two\": 2\n}" == json_object.a_dict()

    def test_object(self, json_object):
        assert {
            'a_string': '"test"',
            'a_digit': '10',
            'a_list': '[1,2,3]',
            'a_dict': '{\n"one": 1,\n"two": 2\n}'
        } == json_object.json()
                

