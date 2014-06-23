from django import template
from django.template import Variable, VariableDoesNotExist
from django.template.loader import get_template

from ..util import get_field_type


register = template.Library()


@register.simple_tag
def setattr(field, attribute, value):
    """
    Sets an attribute on a form field.

    Example Usage::

        {% setattr form.myfield "placeholder" "Email Address" %}
    """
    if not hasattr(field, "field"):
        return ""

    if attribute == "type":
        field.field.widget.input_type = value
    elif attribute == "label":
        field.field.label = value
    elif attribute == "classes":
        cls = field.field.widget.attrs.get("class", "")
        cls += " %s" % value
        field.field.widget.attrs["class"] = cls.strip()
    else:
        field.field.widget.attrs.update({
            attribute: value,
        })

    return ""


@register.simple_tag(takes_context=True)
def formrow(context, field, **kwargs):
    context = context.__copy__()
    widget = field.field.widget

    if kwargs.get("label"):
        field.label = kwargs["label"]

    if kwargs.get("class"):
        widget.attrs["class"] = kwargs["class"]

    template_name = kwargs.get("template")
    if not template_name:
        template_name = context["field_template"]

    t = get_template(template_name)

    input_type = get_field_type(widget)

    context["field"] = field
    context["input_type"] = input_type

    context.update(kwargs)

    return t.render(context)


@register.assignment_tag
def field_type(field):
    return get_field_type(field.field.widget)
