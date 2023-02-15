from django.core.exceptions import ValidationError


def validate_me(value):
    """Проверка равенства значения строке 'me'."""
    if value == 'me':
        raise ValidationError(
            'Использовать имя me в качестве username запрещено.'
        )
    return value
