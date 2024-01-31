from json_decorator import json_class, json_method


test_registry = []

@json_class(test_registry)
class test_me:
	@json_method(registry=test_registry)
	def test():
		return 'test'

