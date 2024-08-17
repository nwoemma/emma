# patients/templatetags/form_tags.py
from django import template

register = template.Library()


@register.filter(name="add_class")
def add_class(field, css_class):
    if hasattr(field, "as_widget"):
        # If field has 'as_widget', it should be a form field
        return field.as_widget(attrs={"class": css_class})
    # Return field unmodified if it's not a form field
    return field


@register.simple_tag
def test_tag():
    return "Test successful!"
