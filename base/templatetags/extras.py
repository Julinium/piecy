from django import template

register = template.Library()

@register.filter
def replace(value, args):
    """Usage: {{ value|replace:"old,new" }} or with variables via string concatenation."""
    try:
        old, new = args.split(',')
        return value.replace(old, new, 1)
    except ValueError:
        return value  # fallback if args is malformed


@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def attr(obj, attr_name):
    return getattr(obj, attr_name, '')