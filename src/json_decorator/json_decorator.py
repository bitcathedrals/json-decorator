# copyright (2022) Michael Mattie (michael.mattie.employers@gmail.com)

from datetime import datetime
from functools import wraps

def _formatter(output):
    if output is None:
        return ""

    if isinstance(output, str):
        return "\"%s\"" % output

    if isinstance(ouptut, dict):
        return 
            "{\n" + 
            ",\n".join(["\"%s\": %s" % (key, _formatter(value)) for key,value in output.items()])
             + "\n}" 

    if isinstance(output, list):
        return "[" + ",".join([_formatter(element) for element in output]) + "]"

    if isinstance(output, datetime):
        return "\"%s\"" % output.isoformat()

    return str(output)


class StaticTypeException(Exception):
    def __init__(*args, **kwargs):
        super().__init__(*args, **kwargs)

def json_fn(wrapped, static=None):

    def generator(wrapped):

        @wraps(wrapped)
        def decorator(*args, **kwargs):
            output = wrapped(*args, **kwargs)

            if static:
                if isinstance(static, dict):
                    return _formatter(static.update(output))

                if isinstance(static, list):
                    return _formatter(output + static)

                raise StaticTypeException(static)
        
            return _formatter(output)
         
        return decorator
    
    return generator
