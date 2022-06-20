from json_decorator.json import _formatter

def sample_dict():
    return {
            "test": {
                "one": 1,
                "two": 2
            }
        }

class TestNested:
    def test_nested_dict(self):
        assert """{
"test": {
"one": 1,
"two": 2
}
}""" == _formatter(sample_dict()).json


