from django.forms import widgets


WIDGETS = (
    (widgets.TextInput, "text"),
    (widgets.HiddenInput, "hidden"),
    (widgets.FileInput, "file"),
    (widgets.Textarea, "textarea"),
    (widgets.CheckboxInput, "checkbox"),
    (widgets.RadioSelect, "radio"),
    (widgets.Select, "select"),
)


def get_field_type(widget):
    try:
        return widget.input_type
    except AttributeError:
        for input_class, field_type in WIDGETS:
            if isinstance(widget, input_class):
                return field_type

    return ""
