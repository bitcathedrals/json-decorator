from json_decorator import jsonify_class, jsonify

@jsonify_class
class test_me:
	@jsonify(json_property=True)
	def test():
		return 'test'
	
	@jsonify
	def no_arg():
		return 'pass'
	

@jsonify_class
class test_bar:
	@jsonify(pre='test more')
	def test():
		return 'test'
	
@jsonify
def test_fn():
	return 'test'
