from django import template

register = template.Library()

@register.filter(name='dir')
def dir_filter(value):
    return dir(value)
