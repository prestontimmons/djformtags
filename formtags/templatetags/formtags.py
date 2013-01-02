import re

from django import template
from django.template import Context, Variable, VariableDoesNotExist
from django.template.loader import get_template


register = template.Library()


@register.simple_tag
def setattr(field, attribute, value):
    """
    Sets an attribute on a form field.

    Example Usage::

        {% setattr form.myfield "placeholder" "Email Address" %}
    """
    if attribute == "type":
        field.field.widget.input_type = value
    elif attribute == "label":
        field.label = value
    else:
        field.field.widget.attrs.update({
            attribute: value,
        })

    return ""


class FormRowNode(template.Node):

    def __init__(self, field, **kwargs):
        self.field = field
        self.kwargs = kwargs

    def render(self, context):
        try:
            field = Variable(self.field).resolve(context)
        except VariableDoesNotExist:
            return ""

        if self.kwargs.get("label"):
            field.label = self.kwargs["label"]

        if self.kwargs.get("class"):
            field.field.widget.attrs["class"] = self.kwargs["class"]

        template_name = self.kwargs.get("template")
        if not template_name:
            template_name = Variable("field_template").resolve(context)

        t = get_template(template_name)

        for entry in context:
            for key in entry:
                self.kwargs.setdefault(key, context[key])

        self.kwargs["field"] = field

        return t.render(Context(self.kwargs))


@register.tag(name="formrow")
def do_formrow(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, \
            "%r tag requires arguments.\n" % token.contents.split()[0]

    arg = args.split(" ")[0]

    kwargs = {}
    for kwarg in token.split_contents()[2:]:
        if "=" in kwarg:
            value = kwarg.split("=")[1]
            if value[0] == value[-1]:
                if value[0] in ["'", '"']:
                    value = value[1:-1]
            kwargs[str(kwarg.split("=")[0])] = value

    return FormRowNode(arg, **kwargs)


class TextFieldNode(template.Node):
    """ An old tag that needs the kabosh. """

    def __init__(self, field, **kwargs):
        self.field = field

        self.field_template = kwargs.get("template")
        self.alternate_label = kwargs.get("label")
        self.autocorrect = kwargs.get("autocorrect")
        self.autocapitalize = kwargs.get("autocapitalize")
        self.help_text = kwargs.get("help_text", "")
        self.placeholder = kwargs.get("placeholder")
        self.rel = kwargs.get("rel")
        self.widget_class = kwargs.get("widget_class")
        self.context = kwargs

    def render(self, context):
        try:
            form_field = Variable(self.field).resolve(context)
        except VariableDoesNotExist:
            return ""

        if self.widget_class:
            c = "%s %s" % (form_field.field.widget.attrs.get('class', ''),
                    self.widget_class)
            c = c.strip()
            form_field.field.widget.attrs['class'] = c

        if form_field.errors:
            c = form_field.field.widget.attrs.get('class', '') + " error"
            form_field.field.widget.attrs['class'] = c

        if self.alternate_label:
            form_field.label = self.alternate_label

        attrs = dict()
        if self.placeholder:
            attrs['placeholder'] = self.placeholder
        if self.autocapitalize:
            attrs['autocapitalize'] = self.autocapitalize
        if self.autocorrect:
            attrs['autocorrect'] = self.autocorrect
        if self.rel:
            attrs['rel'] = self.rel
        form_field.field.widget.attrs.update(attrs)

        # Template name can be specified as an argument to the field
        # or in the template context.
        if self.field_template:
            template_name = self.field_template
        else:
            try:
                template_name = Variable("field_template").resolve(context)
            except VariableDoesNotExist:
                template_name = "formtags/field.html"

        # Required fields can be decorated if required_field_decorator
        # is specified.
        try:
            required_decorator = Variable("required_field_decorator").resolve(context)
        except VariableDoesNotExist:
            required_decorator = None

        t = get_template(template_name)
        return t.render(template.Context(dict(
            field=form_field,
            help_text=self.help_text,
            required_decorator=required_decorator,
            **self.context
        )))



@register.tag(name="render_field")
def do_render_field(parser, token):
    """
    Renders a text input for a form field.

    Example Usage::

        {% render_field form.myfield label="My Label" widget_class="myfield" %}
        {% render_field form.email placeholder="me@example.com" %}
        {% render_field form.date help_text="Format: yyyy-mm-dd" %}
    """
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, \
            "%r tag requires arguments.\n" % token.contents.split()[0]

    arg = args.split(" ")[0]

    kwargs = {}
    for kwarg in token.split_contents()[2:]:
        if "=" in kwarg:
            value = kwarg.split("=")[1]
            if value[0] == value[-1]:
                if value[0] in ["'", '"']:
                    value = value[1:-1]
            kwargs[str(kwarg.split("=")[0])] = value

    return TextFieldNode(arg, **kwargs)
