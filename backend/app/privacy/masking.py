from typing import Any, Dict


# ============================================================
# MASK STRING
# ============================================================

def mask_value(
    value: Any,
    visible_start: int = 2,
    visible_end: int = 2,
    mask_character: str = "*",
) -> str:
    """
    Mask sensitive information while keeping a small
    portion visible.
    """

    if value is None:
        return ""

    text = str(value)

    if len(text) <= visible_start + visible_end:
        return mask_character * len(text)

    middle_length = (
        len(text)
        - visible_start
        - visible_end
    )

    return (
        text[:visible_start]
        + mask_character * middle_length
        + text[-visible_end:]
    )


# ============================================================
# MASK EMAIL
# ============================================================

def mask_email(email: str) -> str:

    if not email or "@" not in email:
        return mask_value(email)

    username, domain = email.split("@", 1)

    if len(username) <= 2:
        masked_username = "*" * len(username)
    else:
        masked_username = (
            username[0]
            + "*" * (len(username) - 2)
            + username[-1]
        )

    return f"{masked_username}@{domain}"


# ============================================================
# MASK PHONE
# ============================================================

def mask_phone(phone: str) -> str:

    digits = "".join(
        character
        for character in str(phone)
        if character.isdigit()
    )

    if len(digits) <= 4:
        return "*" * len(digits)

    return (
        "*" * (len(digits) - 4)
        + digits[-4:]
    )


# ============================================================
# MASK RECORD
# ============================================================

def mask_record(
    record: Dict[str, Any],
    sensitive_fields: list[str],
) -> Dict[str, Any]:
    """
    Mask configured sensitive fields in a record.
    """

    result = dict(record)

    for field in sensitive_fields:

        if field not in result:
            continue

        value = result[field]

        if value is None:
            continue

        if field.lower() == "email":
            result[field] = mask_email(str(value))

        elif field.lower() in {
            "phone",
            "mobile",
            "mobile_number",
        }:
            result[field] = mask_phone(str(value))

        else:
            result[field] = mask_value(value)

    return result