# copyright (2024) Michael Mattie (codermattie@runbox.com)

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

def json_fn(static=None, pre=None, post=None):

    def generator(wrapped):
        
        @wraps(wrapped)
        def json_decorator(*args, **kwargs):
            output = wrapped(*args, **kwargs)

            if static:
                return _formatter(static.update(output)).json

            if pre:
                return _formatter(pre + output).json
        
            if post:
                return _formatter(output + post).json

            return _formatter(output).json
    
        return json_decorator

    return generator

def json_method(static=None, pre=None, post=None, add=None):

    def generator(wrapped):

        if add:
            add.wrap_list(add, wrapped.__name__)
        
        @wraps(wrapped)
        def json_decorator(*args, **kwargs):
            output = wrapped(*args, **kwargs)

            if static:
                return _formatter(static.update(output)).json

            if pre:
                return _formatter(pre + output).json
        
            if post:
                return _formatter(output + post).json

            return _formatter(output).json
    
        return json_decorator

    return generator

def json_class(cls):
    class JsonObject(cls):
        json_wrapped = []

        def wrap_list(cls, name):
            if name in cls.json_wrapped:
                pass
            else:
                cls.json_wrapped.append(name)

        def json_object(self):
            output = {}

            for name in self.__class__:
                method = getattr(self, name)
                output['name'] = method()

    return JsonObject