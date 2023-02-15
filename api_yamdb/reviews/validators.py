from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(year):
    """Проверка значения года выпуска."""
    current_year = timezone.now().year
    if year > current_year:
        raise ValidationError(
            f'Произведение создано позже текущего года {current_year}!'
        )
