from json_decorator.json import _formatter as formatter

class TestFormatter:
    def test_string_bare(self):
        assert '"string"' == formatter("string")

    def test_string_quoted(self):
        assert '"string"' == formatter("\"string\"")

    def test_digit(self):
        assert "10" == formatter(10)

    def test_dict_empty(self):
        assert "{}" == formatter({})

    def test_dict_single(self):
        assert "{\n\"key\": 10\n}" == formatter({"key": 10})

    def test_dict_multiple(self):
        assert "{\n\"first\": 1,\n\"second\": 2\n}" == formatter({'first': 1, 'second': 2})

    def test_list_empty(self):
        assert "[]" == formatter([])

    def test_list_single(self):
        assert "[1]" == formatter([1])

    def test_list_multiple(self):
        assert "[1,2]" == formatter([1,2])


