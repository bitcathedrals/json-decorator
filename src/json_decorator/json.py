# copyright (2022) Michael Mattie (michael.mattie.employers@gmail.com)

from datetime import datetime
from functools import wraps

class Stringified:
    def __init__(self, data, quote=True):
        if not data:
            self.string = ""
            return

        if isinstance(data, Stringified):
            self.string = data.value
            return

        if isinstance(data, str):
            if quote:
                self.string = "\"%s\"" % data
            else:
                self.string = data
            return

        if isinstance(data, datetime):
            self.string = "\"%s\"" % output.isoformat()
            return

        self.string = str(data)

    @property
    def json(self):
        return self.string

def _formatter(output):
    if output is None:
        return Stringified("", quote=False)

    if isinstance(output, dict):
        if not output:
            return Stringified("{}", quote=False)

        return Stringified(\
            "{\n"\
            + ",\n".join(["\"%s\": %s" % (key, _formatter(value).json) for key,value in output.items()])\
            + "\n}",
            quote=False) 

    if isinstance(output, list):
        if not output:
            return Stringified("[]", quote=False)

        return Stringified("[" + ",".join([_formatter(element).json for element in output]) + "]", quote=False)

    return Stringified(output)


def json_fn(static=None, pre=None, post=None):

    def generator(wrapped):

        @wraps(wrapped)
        def decorator(*args, **kwargs):
            output = wrapped(*args, **kwargs)

            if static:
                return _formatter(static.update(output)).json

            if pre:
                return _formatter(pre + output).json
        
            if post:
                return _formatter(output + post).json

            return _formatter(output).json
    
        return decorator

    return generator