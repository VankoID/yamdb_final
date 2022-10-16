from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def year_validator(value):
    """Год выпуска произведения должен быть положителен
    и меньше текущего года."""
    if value < 1 or value > datetime.now().year:
        raise ValidationError(
            _('%(value)s is not a correct year!'),
            params={'value': value},
        )
