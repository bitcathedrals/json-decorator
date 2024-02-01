# copyright (2024) Michael Mattie (codermattie@runbox.com)

from copy import deepcopy
from datetime import datetime

from functools import wraps

class Stringified:
    def __init__(self, data, quote=False):
        if not data:
            self.json = ""
            return

        if isinstance(data, Stringified):
            self.json = data.json
            return

        if isinstance(data, str):
            if quote:
                self.json = "\"%s\"" % data
                return

            self.json = data 
            return

        if isinstance(data, datetime):
            self.json = "\"%s\"" % data.isoformat()
            return

        self.json = str(data)

def _formatter(output):
    if output is None:
        return Stringified("")

    if isinstance(output, dict):
        if not output:
            return Stringified("{}")

        return Stringified("{\n"\
                           + ",\n".join(["\"%s\": %s" % (key, _formatter(value).json) for key,value in output.items()])\
                           + "\n}")

    if isinstance(output, list):
        if not output:
            return Stringified("[]")

        return Stringified("[" + ",".join([_formatter(element).json for element in output]) + "]")

    if isinstance(output, str):
        return Stringified(output, quote=True)

    return Stringified(output)

def _combiner(output):
    if output is None:
        return ""

    if isinstance(output, dict):
        if not output:
            return "{}"

        return "{\n"\
                    + ",\n".join(["\"%s\": %s" % (key, value) for key,value in output.items()])\
                    + "\n}"

    if isinstance(output, list):
        if not output:
            return "[" + ",".join(output) + "]"
            
    return Stringified(output).json

class jsonify:
    def __init__(self, *given, dict=None, pre=None, post=None, json_property=None):
        self.given = given

        if len(given) > 0 and callable(given[0]):
            self.fn = given[0]
        else:
            self.fn = None

        self.dict = dict
        self.pre = pre
        self.post = post
        self.json_property = json_property

    def json_wrapper(self, wrapper, *args, **kwargs):
        print(repr(args))
        print('fn is: ' + repr(wrapper.fn))

        output = wrapper.fn(*args, **kwargs)

        if wrapper.dict:
            merge = deepcopy(wrapper.dict)

            merge.update(output)

            return _formatter(merge).json
            
        if wrapper.pre or wrapper.post:
            merge = []

            if wrapper.pre:
                merge.append(wrapper.pre)

            merge.append(output)

            if wrapper.post:
                merge.append(wrapper.post)

            return _formatter(merge).json

        return _formatter(output).json

    def property_factory(self, fn):
        wrapper = self

        def json_property(*args, **kwargs):
            return wrapper.json_wrapper(wrapper, *args, **kwargs)

        return json_property

    def method_factory(self, fn):
        wrapper = self

        def json_method(*args, **kwargs):
            return wrapper.json_wrapper(wrapper, *args, **kwargs)
        
        return json_method

    def __call__(self, *params, **kwargs):
        if len(params) == 1 and callable(params[0]):
            self.fn = params[0]

            if self.json_property:
                return self.property_factory(params[0])
            else:
                return self.method_factory(params[0])
        else:
            return _formatter(self.fn(*params, **kwargs)).json
        
def jsonify_object(self):
    output = {}

    for name in dir(self.__class__):
        entry = getattr(self.__class__, name)
        if callable(entry) and hasattr(entry, '__qualname__'):
            outer = entry.__qualname__.split('.')[-1]

            print("name is %s outer is %s full is %s" % (name, outer, entry.__qualname__))

            if 'json_property' == outer:
                output[name] = getattr(self, name)()
        
    if output:    
        return _combiner(output)

    return ""

def jsonify_class(cls):
    cls.json = jsonify_object

    return cls
