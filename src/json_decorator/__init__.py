# copyright (2024) Michael Mattie (codermattie@runbox.com)

from copy import deepcopy
from datetime import datetime

from functools import wraps

class Stringified:
    def __init__(self, data, quote=False):
        if data is None:
            self.json = ''
            return

        if isinstance(data, Stringified):
            self.json = data.json
            return

        if isinstance(data, str):
            self.json = data
        else:
            if isinstance(data, datetime):
                self.json = f'"%s"' % data.isoformat()
            else:
                self.json = str(data)

        if quote:
            self.json = f'"%s"' % self.json

def _formatter(output):
    if output is None:
        return Stringified(None)

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

def _isfunction(x):
    return isinstance(x, type(lambda: None))

def _isclass(x):
    return isinstance(x, type)

def _jsonify_object(self):
    output = {}
    cls=self.__class__

    for name in dir(cls):
        entry = getattr(cls, name)
        
        if _isfunction(entry) and hasattr(entry, 'json_property') and entry.json_property:
            if isinstance(entry.json_property, str):
                field_name = entry.json_property
            else:
                field_name = name

            output[field_name] = getattr(self, name)()
        
    if output:    
        return _combiner(output)

    return ""


def _json_wrapper(*args, _wrapper=None, **kwargs):
    fn = _wrapper.fn
    output = fn(*args, **kwargs)

    if _wrapper.dict:
        merge = deepcopy(_wrapper.dict)

        merge.update(output)

        return _formatter(merge).json
            
    if _wrapper.pre or _wrapper.post:
        merge = []

        if _wrapper.pre:
            merge.append(_wrapper.pre)

        merge.append(output)

        if _wrapper.post:
            merge.append(_wrapper.post)

        return _formatter(merge).json

    return _formatter(output).json

class jsonify:
    def set_fn(self, fn):
        self.fn = fn

        self.fn.json_property = self.json_property

        self.fn_short_name = self.fn.__name__
        self.fn_long_name = self.fn.__qualname__

        #print(f'fn short is: %s fn long is: %s' % (self.fn_short_name, self.fn_long_name))

    def __init__(self, *given, dict=None, pre=None, post=None, p=None):
        self.given = given

        self.dict = dict
        self.pre = pre
        self.post = post
        self.json_property = p

        self.cls = None
        self.fn = None

        if len(given) > 0:
            first_arg = given[0]

            if _isfunction(first_arg):
                self.set_fn(first_arg)
                return
        
            if _isclass(first_arg):
                self.cls = first_arg

    def property_factory(self):

        @wraps(self.fn)
        def json_property(*args, **kwargs):
            return _json_wrapper(*args, _wrapper=self, **kwargs)

        return json_property

    def method_factory(self):

        @wraps(self.fn)
        def json_method(*args, **kwargs):
            return _json_wrapper(*args, _wrapper=self, **kwargs)
        
        return json_method
    
    def __call__(self, *params, **kwargs):        
        if self.cls:
            self.cls.json = _jsonify_object
            return self.cls(*params, **kwargs)
        
        if len(params) == 1:
            single_arg = params[0]
            
            if _isfunction(single_arg):
                self.set_fn(single_arg)

                if self.json_property:
                    return self.property_factory()
            
                return self.method_factory()
        
        fn = self.fn
        return _formatter(fn(*params, **kwargs)).json

