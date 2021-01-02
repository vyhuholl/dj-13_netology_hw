from django import template

register = template.Library()


@register.filter()
def get_type(obj):
    return type(obj).__name__
