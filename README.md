<img src="https://krywok.com/svg/logo/full-mix-white-alpha.svg" alt="Krywok Logo" width="190" height="55" />

**Krywok Codetable** provides centralized, standardized response codes for APIs and applications. It ensures consistency by treating codes as a single source of truth.

## Installation

```bash
pip install krywok-codetable
```

## Why use this?

Managing response codes and messages across an application can become chaotic. **Krywok Codetable** allows you to:

1.  **Centralize** all your application codes and messages in one place.
2.  **Standardize** API responses with consistent error codes and messages.
3.  **Internationalize (i18n)** messages easily, switching languages dynamically.
4.  **Inject dynamic data** into messages using a simple formatting API.

## Usage Example

### Defining Codetables

You can organize your codes into multiple classes for better structure, even while sharing the same namespace.

```python
from codetable import Codetable, msg, i18n

# 1. Set the base locale (Critical for i18n)
i18n.set_base_locale("en")

class UserError(Codetable):
    NAMESPACE = "user"

    NOT_FOUND = msg("User not found.")

    LOCKED = msg("Account locked for {minutes} minutes.")

    ALREADY_EXISTS = i18n(
        en="User already exists.",
        pl="Użytkownik już istnieje.",
    )

class UserSuccess(Codetable):
    NAMESPACE = "user"

    CREATED = msg("User created successfully.")

    UPDATED = i18n(
        en="User updated successfully.",
        pl="Użytkownik został zaktualizowany pomyślnie.",
    )
```

### Accessing Codes

```python
# --- 1. Accessing Standard Codes ---
print(UserError.NOT_FOUND)
# Output: {'code': 'user.not_found', 'msg': 'User not found.'}

# --- 2. Dynamic Formatting ---
print(UserError.format(UserError.LOCKED, minutes=15))
# Output: {'code': 'user.locked', 'msg': 'Account locked for 15 minutes.'}

# --- 3. Accessing i18n Codes (Default: English, i18n.set_base_locale("en")) ---
print(UserError.ALREADY_EXISTS)
# Output: {'code': 'user.already_exists', 'msg': 'User already exists.'}

# --- 4. Switching Locales (for all i18n codes) ---
i18n.set_locale("pl")

print(UserError.ALREADY_EXISTS)
# Output: {'code': 'user.already_exists', 'msg': 'Użytkownik już istnieje.'}
```

### Lazy Load

```python
i18n.set_locale("en")

error = UserError.lazy("ALREADY_EXISTS")

print(error())
# Output: {'code': 'user.already_exists', 'msg': 'User already exists.'}

success = UserSuccess.lazy("UPDATED")

print(success())
# Output: {'code': 'user.updated', 'msg': 'User updated successfully.'}
```

### Customizing Key Maps

You can customize output keys globally or per-table by modifying the `key_map`.

```python
# Change default keys globally
Codetable.key_map = {"code": "error_code", "value": "message"}

print(UserError.NOT_FOUND)
# Output: {'error_code': 'user.not_found', 'message': 'User not found.'}
```

## Core Features

- **Namespace Management**: Automatically prefixes codes with the table's namespace (e.g., `user.not_found`).
- **Dynamic Formatting**: Supports injecting data into messages via `*args` and `**kwargs` using the `.format()` method.
- **Strict Typing**: Built with Python type hints for excellent IDE support.
- **Dynamic Descriptor Protocol**: Codes know their own variable names and parent tables automatically.
- **Context-Aware I18n**: Uses `contextvars` to handle per-request locales safely in async environments (e.g., FastAPI).
- **Customizable Output**: Easily remap dictionary keys to match your existing API schema.
