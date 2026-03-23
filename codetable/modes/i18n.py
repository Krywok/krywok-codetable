from krywok_kit_localize import Localize

from codetable.core.code import Code


class i18n(Code, Localize):
    """
    A Code implementation that supports internationalization (i18n).

    This class allows defining messages for different locales and retrieving the
    appropriate message based on the current context locale.
    """
    def __init__(self, **msg: str) -> None:
        """
        Initializes an i18n Code instance with messages for different locales.

        Args:
            **msg (str): Keyword arguments mapping locale codes to message strings.
        """
        super().__init__()

        self.msg: dict[str, str] = msg

    def compute_value(self) -> str:
        """
        Computes the localized message based on the current locale.

        Returns:
            str: The message corresponding to the current locale, or the base locale
                if the current locale is not available.
        """
        return self.resolve_translation(data=self.msg)
