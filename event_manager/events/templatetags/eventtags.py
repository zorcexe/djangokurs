"""
In dieser Datei werden Filter und Tags für die Events-App angelegt.
"""

from django import template
from user.models import User

register = template.Library()


@register.filter()
def has_group(user: User, group_name: str) -> bool:
    """Ein Template-Filter, der True zurückgibt,
    wenn ein User Mitglied einer Gruppe ist.

    if request.user|has_group:"Moderatoren"
    """
    return user.groups.filter(name=group_name).exists()
