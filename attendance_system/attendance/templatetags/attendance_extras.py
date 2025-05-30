from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Get an item from a dictionary using bracket notation.
    Usage: {{ mydict|get_item:item_key }}
    """
    if dictionary is None:
        return None
    
    if isinstance(key, int):
        key = int(key)
    
    try:
        return dictionary.get(key)
    except (AttributeError, KeyError, TypeError):
        return None

@register.filter
def percentage(value, total):
    """
    Calculate percentage.
    Usage: {{ value|percentage:total }}
    """
    try:
        value = float(value)
        total = float(total)
        if total > 0:
            return round((value / total) * 100, 1)
        return 0
    except (ValueError, ZeroDivisionError, TypeError):
        return 0 