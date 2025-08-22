from django import template

register = template.Library()

@register.filter
def to(value):
    if isinstance(value, int):
        return range(value)
    return []

@register.filter
def startswith(value, arg):
    """Check if a string starts with a given prefix."""
    if isinstance(value, str):
        return value.startswith(arg)
    return False