Form Tags
=========

Template tags for rendering Django forms.

Usage
-----

Rendering fields in a template::

    {% load formtags %}

    {% render_field form.myfield label="My Label" widget_class="myfield" %}
    {% render_field form.email placeholder="me@example.com" %}
    {% render_field form.date help_text="Format: yyyy-mm-dd" %}

Adding a required field decorator::

    {% with required_field_decorator="*" %}
      {% render_field form.first_name %}
      {% render_field form.last_name %}
    {% endwith %}

Rendering fields with a custom template::

    {% render_field form.country template="mytemplate.html" %}

    {% with field_template="myothertemplate.html" %}
      {% render_field form.address1 %}
      {% render_field form.address2 %}
    {% endwith %}
