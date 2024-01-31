# copyright (2024) Michael Mattie (codermattie@runbox.com)

from datetime import datetime

from functools import wraps
from decorator import decorator

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

def json_method(static=None, pre=None, post=None, registry=None):

    def generator(wrapped):

        if registry is not None:
            name = wrapped.__name__

            if name not in registry:
                registry.append(name)
        
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

def json_class(registry):

    @decorator
    def factory(cls):

        class JsonObjectClass(cls):
            def json(self):
                output = {}

                if registry:
                    for name in registry:
                        method = getattr(self, name)
                        output[name] = method()
            
                return output
            
        return JsonObjectClass

    return factory