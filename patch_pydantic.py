import pydantic.typing

if hasattr(pydantic.typing.ForwardRef, '_evaluate'):
    original_evaluate = pydantic.typing.ForwardRef._evaluate

    def patched_evaluate(self, globalns, localns, recursive_guard=set()):
        return original_evaluate(self, globalns, localns, recursive_guard=recursive_guard)

    pydantic.typing.ForwardRef._evaluate = patched_evaluate
