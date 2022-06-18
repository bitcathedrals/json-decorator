from json_decorator.json import _formatter as formatter

class TestFormatter:
    def test_string(self):
        assert '"string"' == formatter("string").json

    def test_digit(self):
        assert "10" == formatter(10).json

    def test_dict_empty(self):
        assert "{}" == formatter({}).json

    def test_dict_single(self):
        assert "{\n\"key\": 10\n}" == formatter({"key": 10}).json

    def test_dict_multiple(self):
        assert "{\n\"first\": 1,\n\"second\": 2\n}" == formatter({'first': 1, 'second': 2}).json

    def test_list_empty(self):
        assert "[]" == formatter([]).json

    def test_list_single(self):
        assert "[1]" == formatter([1]).json

    def test_list_multiple(self):
        assert "[1,2]" == formatter([1,2]).json


