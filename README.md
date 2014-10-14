# Control Django form field rendering from within the template

This app provides template tags that simplify and enhance form rendering
in Django templates.

## One: Set custom attributes on a form field

Say you have the following form with an email field. 

```python
class EmailForm(forms.Form):
    email = forms.CharField(max_length=256)
```

Now, you want to reuse this form, but optimized for a mobile device. Let's
do it in the form class:

```python
class EmailField(forms.TextInput):
    input_type = "email"

class MobileEmailForm(EmailForm):
    email = forms.CharField(
        widget=forms.TextInput(attrs={
            "autocapitalize": "off",
            "class": "mobile-input",
            "placeholder": "me@example.com",
        ),
    )
```

Really? That's ugly, it requires a new form definition, and it's messing
with stuff that belongs in the template.

Enter {% setattr %}:

```html
{% load formtags %}

{% setattr form.email "type" "email" %}
{% setattr form.email "autocapitalize" "off" %}
{% setattr form.email "class" "mobile-input" %}
{% setattr form.email "placeholder" "me@example.com" %}
{{ form.email }}
```

And you get:

```
<input type="email" name="email" maxlength="256" autocapitalize="off" placeholder="me@example.com" class="mobile-input" id="id_email" />
```

Set whatever attribute you want directly on the field right in the template
where you're rendering the form. No boilerplate needed.

### Special attributes

In addition to setting an attribute, the following settings will modify
the field or widget:

* type 
* label 
* initial 
* classes

Note: Using the `classes` argument will set the class to the field in
addition to the existing field class. Using `class` will override the
field class.


## Two: Rendering form rows

This tag is more convenience than anything.

Start with a basic form row template, ``forms/row.html``:

```html
<div class="form-row">
  <div class="formrow-label">
    <label for="{{ field.auto_id }}" class="label {% if field.field.required %}label-required{% else %}label-optional{% endif %}">
      {{ field.label|safe }}
    </label>
    {% if label_help_text %}<div class="form-row-label-help-text">{{ label_help_text|safe }}</div>{% endif %}
  </div>
  <div class="formrow-input">
    {% if field.errors %}
      <div class="form-row-error-message"><i class="fa fa-warning"></i> {{ field.errors.0 }}</div>
    {% endif %}

    {{ field }}
  </div>
</div>
```

Enter {% formrow %}:

```html
{% formrow form.email %}
```

You can also pass in a couple common arguments. Any extra values are passed
directly to the form row template context.

```html
{% formrow form.email class="input-email" label="Email Address" template="formrow.html" foo="bar" %}
```

The template will also be rendered with an ``input_type`` variable in the
context. This can be used to customize rendering for different field types.

```
{% if input_type == "checkbox" %}
  .. handle checkbox
{% elif input_type == "radio" %}
  .. handle radio
{% elif input_type == "text" %}
  .. handle text
{% endif %}
```

Input type is one of the following:

```
checkbox
file
hidden
radio
select
text
textarea
```

## Installation

Install with pip:

```
pip install djformtags
```

Or install from github

```
pip install -e git+git@github.com:prestontimmons/djformtags.git#egg=djformtags
```

Add ``djformtags`` to ``INSTALLED_APPS``.
