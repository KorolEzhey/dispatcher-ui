from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key, 0)
    return 0


@register.filter
def percent(value, total):
    try:
        return round(int(value) / int(total) * 100, 1)
    except (ValueError, ZeroDivisionError, TypeError):
        return 0
