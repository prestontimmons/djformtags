from django import forms
from django.http import HttpRequest
from django.template import Template, Context
from django.test import TestCase
from django.test.utils import (
    setup_test_template_loader,
    restore_template_loaders,
)


class TestForm(forms.Form):
    field = forms.CharField(max_length=100)


class FormRowTemplateTagTest(TestCase):

    def setUp(self):
        templates = {
            "field.html": Template("{{ field }}"),
            "context.html": Template("{{ variable }}"),
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
            '<input id="id_field" type="text" name="field" maxlength="100" />',
        )

    def test_maintain_context(self):
        template = Template('{% load formtags %}{% formrow form.field template="context.html" %}')
        form = TestForm()
        context = Context(dict(form=form, variable="variable"))
        self.assertEqual(
            template.render(context),
            'variable',
        )


class SetAttrTemplateTagTest(TestCase):

    def test_setattr(self):
        template = Template('{% load formtags %}{% setattr form.field \'placeholder\' "Email Address" %}{{ form.field }}')
        context = Context(dict(
            form=TestForm(),
            request=HttpRequest(),
        ))
        self.assertEqual(
            template.render(context),
            '<input id="id_field" type="text" placeholder="Email Address" name="field" maxlength="100" />'
        )

    def test_set_input_type(self):
        template = Template('{% load formtags %}{% setattr form.field "type" "email" %}{{ form.field }}')
        context = Context(dict(
            form=TestForm(),
            request=HttpRequest(),
        ))
        self.assertEqual(
            template.render(context),
            '<input id="id_field" type="email" name="field" maxlength="100" />',
        )

    def test_set_label(self):
        template = Template('{% load formtags %}{% setattr form.field "label" "Email Address" %}{{ form.field.label_tag }}')
        context = Context(dict(
            form=TestForm(),
            request=HttpRequest(),
        ))
        self.assertEqual(
            template.render(context),
            '<label for="id_field">Field</label>',
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
            '<input id="id_field" type="text" name="field" maxlength="100" />\ntest\n',
            template.render(Context(dict(form=form, request=request))),
        )


