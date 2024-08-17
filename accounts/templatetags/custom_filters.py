# your_app/templatetags/custom_filters.py
from django import template

register = template.Library()


@register.filter(name="add_class")
def add_class(value, arg):
    return value.as_widget(attrs={"class": arg})


@register.filter
def has_attr(obj, attr_name):
    return has_attr(obj, attr_name)
