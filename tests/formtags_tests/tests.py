from django import forms
from django.http import HttpRequest
from django.template import Context, Template, TemplateDoesNotExist
from django.test import TestCase
from django.test.utils import (
    setup_test_template_loader,
    restore_template_loaders,
)

from formtags.util import get_field_type


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


class RenderFieldTemplateTagTest(TestCase):
    """ The oldies. """

    def test_display_render_field(self):
        template = Template("{% load formtags %}{% render_field form.field %}")
        request = HttpRequest()
        form = TestForm()
        self.assert_('input' in \
            template.render(Context(dict(form=form, request=request))))

    def test_display_render_field_with_attributes(self):
        template = Template('{% load formtags %}{% render_field form.field widget_class=myclass rel=myrel label="My Label" placeholder="fill in here" %}')
        request = HttpRequest()
        form = TestForm()
        content = template.render(Context(dict(form=form, request=request)))
        self.assert_('rel="myrel"' in content)
        self.assert_('placeholder="fill in here"' in content)
        self.assert_('class="myclass"' in content)
        self.assert_('My Label' in content)

    def test_display_render_field_with_single_quotes(self):
        template = Template("{% load formtags %}{% render_field form.field widget_class='myclass' rel=myrel label='My Label' %}")
        request = HttpRequest()
        form = TestForm()
        content = template.render(Context(dict(form=form, request=request)))
        self.assert_('rel="myrel"' in content)
        self.assert_('class="myclass"' in content)

    def test_display_render_field_ignores_internal_quotes(self):
        template = Template("{% load formtags %}{% render_field form.field label=\"Friend's Email\" %}")
        request = HttpRequest()
        form = TestForm()
        content = template.render(Context(dict(form=form, request=request)))
        self.assert_("Friend&#39;s Email" in content)

    def test_display_render_field_ignore_non_kwargs(self):
        template = Template('{% load formtags %}{% render_field form.field "Some arg" %}')
        request = HttpRequest()
        form = TestForm()
        content = template.render(Context(dict(form=form, request=request)))
        self.assert_("input" in content)

    def test_define_template_from_context(self):
        template = Template("{% load formtags %}{% with 'formtags/field.html' as field_template %}{% render_field form.field placeholder='Test' %}{% endwith %}")
        request = HttpRequest()
        form = TestForm()
        self.assert_('input' in \
            template.render(Context(dict(form=form, request=request))))

    def test_no_form(self):
        template = Template("{% load formtags %}{% render_field form.field %}")
        request = HttpRequest()
        self.assertEqual(template.render(Context(dict(request=request))), "")

    def test_kwargs(self):
        template = Template("{% load formtags %}{% render_field form.field keyword='test' template='formtags/test.html' %}")
        request = HttpRequest()
        form = TestForm()
        self.assertEqual(
            template.render(Context(dict(form=form, request=request))),
            '<input id="id_field" maxlength="100" name="field" type="text" />\ntest\n',
        )
