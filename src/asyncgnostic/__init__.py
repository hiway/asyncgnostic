import inspect as _inspect
from typing import Optional as _Optional


def is_async(stack_depth: _Optional[int]=None):
    stack = _inspect.stack()[1:]
    for i, frame in enumerate(stack):
        func_name = frame.function
        
        if func_name == "<module>":
            continue

        if stack_depth and i == stack_depth:
            break

        for frame in _inspect.stack()[1:]:
            if func_name in frame.frame.f_locals:
                func = frame.frame.f_locals[func_name]
                if _inspect.iscoroutinefunction(func):
                    return True

    return False