from json_decorator import jsonify

@jsonify
class test_me:
	@jsonify(p=True)
	def test(self):
		return 'test'
	
	@jsonify
	def no_arg(self):
		return 'pass'
	
@jsonify
class test_bar:
	@jsonify(pre='test more')
	def test(self):
		return 'test'
	
@jsonify
def test_fn():
	return 'test'
