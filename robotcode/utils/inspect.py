from typing import Any, Callable, Iterator, List, Optional
import inspect


def iter_methods(
    obj: Any, predicate: Optional[Callable[[Callable[..., Any]], bool]] = None
) -> Iterator[Callable[..., Any]]:
    is_cls = inspect.isclass(obj)
    cls = obj if is_cls else type(obj)

    for name in dir(cls):
        v = getattr(cls, name)
        if inspect.isfunction(v):
            if is_cls:
                m = v
            else:
                m = getattr(obj, name)
                if not inspect.ismethod(m):
                    continue

            if predicate is None or predicate(m):
                yield m


def get_methods(
    instance_or_type: Any, predicate: Optional[Callable[[Callable[..., Any]], bool]] = None
) -> List[Callable[..., Any]]:
    return [m for m in iter_methods(instance_or_type, predicate)]


_lambda_type = type(lambda: 0)
_lamda_name = (lambda: 0).__name__


def is_lambda(v: Any) -> bool:
    return isinstance(v, _lambda_type) and v.__name__ == _lamda_name