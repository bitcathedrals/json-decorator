# copyright (2022) Michael Mattie (michael.mattie.employers@gmail.com)

from datetime import datetime
from functools import wraps

def _formatter(output):
    if output is None:
        return ""

    if isinstance(output, str):
        if output[0] == "\"":
            return output

        return "\"%s\"" % output

    if isinstance(output, dict):
        if not output:
            return "{}"

        return "{\n"\
            + ",\n".join(["\"%s\": %s" % (key, _formatter(value)) for key,value in output.items()])\
            + "\n}" 

    if isinstance(output, list):
        if not output:
            return "[]"

        return "[" + ",".join([_formatter(element) for element in output]) + "]"

    if isinstance(output, datetime):
        return "\"%s\"" % output.isoformat()

    return str(output)


def json_fn(static=None, pre=None, post=None):

    def generator(wrapped):

        @wraps(wrapped)
        def decorator(*args, **kwargs):
            output = wrapped(*args, **kwargs)

            if static:
                return _formatter(static.update(output))

            if pre:
                return _formatter(pre + output)
        
            if post:
                return _formatter(output + post)

            return _formatter(output)
    
        return decorator

    return generator