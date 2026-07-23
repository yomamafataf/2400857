MIN_LENGTH = 10
MAX_LENGTH = 128


def validate_password(password, is_common):
    """Return OWASP C7 password-policy errors for a supplied password."""
    if not isinstance(password, str):
        return ["Password is required."]

    errors = []
    if len(password) < MIN_LENGTH:
        errors.append(f"Use at least {MIN_LENGTH} characters.")
    if len(password) > MAX_LENGTH:
        errors.append(f"Use no more than {MAX_LENGTH} characters.")
    if any(not character.isprintable() for character in password):
        errors.append("Control characters are not allowed.")
    if not errors and is_common(password):
        errors.append("This password appears in the common-password blocklist.")
    return errors
