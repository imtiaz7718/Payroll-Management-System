from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Custom filter to access dictionary items in templates.
    Usage: {{ dictionary|get_item:key }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key, None)
    return None
