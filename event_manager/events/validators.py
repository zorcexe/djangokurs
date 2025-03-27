from datetime import timedelta, datetime
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def datetime_in_future(offset_hours: int, value: datetime) -> None:
    """Prüft, ob ein Zeitpunkt in der Zukunft liegt. offset Stunden"""
    if value <= timezone.now() + timedelta(hours=offset_hours):
        raise ValidationError(
            f"Zeitpunkt muss mindestens {offset_hours} in der Zukunft liegen"
        )
