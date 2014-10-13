from django import forms
from django.http import HttpRequest
from django.template import Context, Template, TemplateDoesNotExist
from django.test import TestCase
from django.test.utils import (
    setup_test_template_loader,
    restore_template_loaders,
)

from .util import get_field_type


class TestForm(forms.Form):
    field = forms.CharField(max_length=100)


class GetFieldTypeTest(TestCase):

    def test_text(self):
        self.assertEqual(get_field_type(forms.TextInput()), "text")

    def test_hidden(self):
        self.assertEqual(get_field_type(forms.HiddenInput()), "hidden")

    def test_file(self):
        self.assertEqual(get_field_type(forms.FileInput()), "file")

    def test_textarea(self):
        self.assertEqual(get_field_type(forms.Textarea()), "textarea")

    def test_checkbox(self):
        self.assertEqual(get_field_type(forms.CheckboxInput()), "checkbox")

    def test_select(self):
        self.assertEqual(get_field_type(forms.Select()), "select")

    def test_radio(self):
        self.assertEqual(get_field_type(forms.RadioSelect()), "radio")


class FieldTypeTagTest(TestCase):

    def test_text(self):
        template = Template("{% load formtags %}{% field_type form.field as type %}{{ type }}")
        form = TestForm()
        context = Context(dict(form=form))
        self.assertEqual(
            template.render(context),
            "text",
        )


class FormRowTemplateTagTest(TestCase):

    def setUp(self):
        templates = {
            "field.html": Template("{{ field }}"),
            "field-type.html": Template("{{ input_type }}"),
            "label.html": Template("{{ field.label }}"),
            "context.html": Template("{{ variable }}"),
            "kwargs.html": Template("{{ x }} {{ y }}"),
        }
        setup_test_template_loader(templates)

    def tearDown(self):
        restore_template_loaders()

    def test_form_row(self):
        template = Template('{% load formtags %}{% formrow form.field template="field.html" %}')
        form = TestForm()
        context = Context(dict(form=form))
        self.assertEqual(
            template.render(context),
            '<input id="id_field" maxlength="100" name="field" type="text" />',
        )

    def test_input_type(self):
        template = Template('{% load formtags %}{% formrow form.field template="field-type.html" %}')
        form = TestForm()
        context = Context(dict(form=form))
        self.assertEqual(
            template.render(context),
            'text',
        )

    def test_label(self):
        template = Template('{% load formtags %}{% formrow form.field label="New Label" template="label.html" %}')
        form = TestForm()
        context = Context(dict(form=form))
        self.assertEqual(
            template.render(context),
            "New Label",
        )

    def test_class(self):
        template = Template('{% load formtags %}{% formrow form.field class="input-text" template="field.html" %}')
        form = TestForm()
        context = Context(dict(form=form))
        self.assertEqual(
            template.render(context),
            '<input class="input-text" id="id_field" maxlength="100" name="field" type="text" />',
        )

    def test_classes(self):
        template = Template('{% load formtags %}{% formrow form.field classes="input-text" template="field.html" %}')
        form = TestForm()
        context = Context(dict(form=form))
        self.assertEqual(
            template.render(context),
            '<input class="input-text" id="id_field" maxlength="100" name="field" type="text" />',
        )

    def test_field_template(self):
        template = Template('{% load formtags %}{% with field_template="label.html" %}{% formrow form.field %}{% endwith %}')
        form = TestForm()
        context = Context(dict(form=form))
        self.assertEqual(
            template.render(context),
            'Field',
        )

    def test_maintain_context(self):
        template = Template('{% load formtags %}{% formrow form.field template="context.html" %}')
        form = TestForm()
        context = Context(dict(form=form, variable="variable"))
        self.assertEqual(
            template.render(context),
            "variable",
        )

    def test_kwargs(self):
        template = Template('{% load formtags %}{% formrow form.field template="kwargs.html" x="1" y="2" %}')
        form = TestForm()
        context = Context(dict(form=form))
        self.assertEqual(
            template.render(context),
            "1 2",
        )

    def test_template_missing(self):
        template = Template('{% load formtags %}{% formrow form.field template="missing.html" %}')
        form = TestForm()
        context = Context(dict(form=form))
        with self.assertRaises(TemplateDoesNotExist):
            template.render(context)


class SetAttrTemplateTagTest(TestCase):

    def test_setattr(self):
        template = Template('{% load formtags %}{% setattr form.field "placeholder" "Email Address" %}{{ form.field }}')
        context = Context(dict(
            form=TestForm(),
            request=HttpRequest(),
        ))
        self.assertEqual(
            template.render(context),
            '<input id="id_field" maxlength="100" name="field" placeholder="Email Address" type="text" />',
        )

    def test_classes(self):
        template = Template('{% load formtags %}{% setattr form.field "classes" "one" %}{% setattr form.field "classes" "two" %}{{ form.field }}')
        context = Context(dict(
            form=TestForm(),
            request=HttpRequest(),
        ))
        self.assertEqual(
            template.render(context),
            '<input class="one two" id="id_field" maxlength="100" name="field" type="text" />',
        )

    def test_empty(self):
        template = Template('{% load formtags %}{% setattr form.field "placeholder" "Email Address" %}{{ form.field }}')
        context = Context(dict(
            request=HttpRequest(),
        ))
        self.assertEqual(
            template.render(context),
            ""
        )

    def test_set_input_type(self):
        template = Template('{% load formtags %}{% setattr form.field "type" "email" %}{{ form.field }}')
        context = Context(dict(
            form=TestForm(),
            request=HttpRequest(),
        ))
        self.assertEqual(
            template.render(context),
            '<input id="id_field" maxlength="100" name="field" type="email" />',
        )

    def test_set_label(self):
        template = Template('{% load formtags %}{% setattr form.field "label" "Email Address" %}{{ form.field.label }}')
        context = Context(dict(
            form=TestForm(),
            request=HttpRequest(),
        ))
        self.assertEqual(
            template.render(context),
            'Email Address',
        )

    def test_set_initial(self):
        template = Template('{% load formtags %}{% setattr form.field "initial" "broman@gfa.org" %}{{ form.field.field.initial }}')
        context = Context(dict(
            form=TestForm(),
            request=HttpRequest(),
        ))
        self.assertEqual(
            template.render(context),
            "broman@gfa.org",
        )
