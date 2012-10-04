Provides control of Django form field rendering from within the template
========================================================================

This app provides two minimal template tags that simplify and enhance form rendering in Django templates.

One: Set custom attributes on a form field
------------------------------------------

Say you have the following form with an email field. 

```python
class EmailForm(forms.Form):
    email = forms.CharField(max_length=256)
```

Now, you want to reuse this form, but optimized for a mobile device. Let's do it in the form class:

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

Really? That's ugly, it requires a new form definition, and it's messing with stuff that belongs in the template.

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

Set whatever attribute you want directly on the field right in the template where you're rendering the form. No boilerplate needed.


Two: Rendering form rows
------------------------

This tag is more convenience than anything.

Start with a basic form row template, formrow.html:

```html
<div class="form-row">
  {% if field.errors %}<div class="form-row-message">{{ field.errors.0 }}</div>{% endif %}
  {{ field.label_tag }}
  {{ field }}
</div>
```

Enter {% formrow %}:

```html
{% formrow form.email template="formrow.html" %}
```

You can also pass in a couple common arguments, or pass any values to the form row template.

```html
{% formrow form.email class="input-email" label="Email Address" template="formrow.html" %}
```

And...
------

The end.
