from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from codetable.core.resources.types import CodeResult

if TYPE_CHECKING:
    from typing import Any, ClassVar

    from .resources.types import KeyMap


class Codetable:
    """
    A base class representing a Codetable, which serves as a namespace for standardizing codes.

    Attributes:
        NAMESPACE (ClassVar[str]): The namespace identifier for the Codetable.
        key_map (KeyMap): A mapping dictionary that defines the keys for 'code' and 'value'
            in the output dictionary. Defaults to map "code" to "code" and "value" to "msg".
    """

    NAMESPACE: ClassVar[str]

    key_map: KeyMap = {"code": "code", "value": "msg"}

    @classmethod
    def lazy(cls, code: str) -> Callable[[], CodeResult]:
        """
        Creates a deferred evaluator for a specific code instance.

        This method retrieves a Code instance from the class dictionary and returns 
        a callable that, when invoked, triggers the actual data retrieval or 
        computation (via the `__get__` descriptor protocol).

        Args:
            code: The string key representing the attribute name of the 
                Code instance to be lazily loaded.

        Returns:
            A zero-argument callable that returns a `CodeResult` when called.

        Raises:
            RuntimeError: If the attribute associated with `code` is not an 
                instance of the `Code` class.
        """
        from codetable.core.code import Code

        instance: Any = cls.__dict__.get(code)

        if not isinstance(instance, Code):
            raise RuntimeError("Code instances can only be lazy loaded.")

        return lambda: instance.__get__()

    @classmethod
    def format(cls, result: CodeResult, /, *args, **kwargs) -> CodeResult:
        """
        Formats the value template within a CodeResult using provided arguments.

        This method retrieves the template string from the CodeResult and
        applies standard Python string formatting. It supports both positional 
        placeholders and named keyword arguments.

        Args:
            result: The CodeResult containing the value template to format.
            *args: Variable length argument list for positional placeholders.
            **kwargs: Arbitrary keyword arguments for named placeholders.

        Returns:
            The modified CodeResult with the formatted value string.
        """
        value_key: str = cls.key_map["value"]

        result[value_key] = result[value_key].format(*args, **kwargs)

        return result
