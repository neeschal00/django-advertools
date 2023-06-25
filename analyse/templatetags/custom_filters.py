from django import template

register = template.Library()


@register.filter
def get_nested_value(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
