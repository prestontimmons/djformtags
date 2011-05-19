from django import forms
from django.http import HttpRequest
from django.template import Template, Context
from django.test import TestCase


class TestForm(forms.Form):
    field = forms.CharField(max_length=100)


class TextFieldTemplateTagTest(TestCase):

    def test_display_text_field(self):
        template = Template("{% load form_tags %}{% text_field form.field %}")
        request = HttpRequest()
        form = TestForm()
        self.assert_('input' in \
            template.render(Context(dict(form=form, request=request))))

    def test_display_text_field_with_attributes(self):
        template = Template('{% load form_tags %}{% text_field form.field class_name=myclass rel=myrel label="My Label" placeholder="fill in here" %}')
        request = HttpRequest()
        form = TestForm()
        content = template.render(Context(dict(form=form, request=request)))
        self.assert_('rel="myrel"' in content)
        self.assert_('placeholder="fill in here"' in content)
        self.assert_('class="myclass"' in content)
        self.assert_('My Label' in content)

    def test_display_text_field_with_single_quotes(self):
        template = Template("{% load form_tags %}{% text_field form.field class_name='myclass' rel=myrel label='My Label' %}")
        request = HttpRequest()
        form = TestForm()
        content = template.render(Context(dict(form=form, request=request)))
        self.assert_('rel="myrel"' in content)
        self.assert_('class="myclass"' in content)

    def test_display_text_field_ignores_internal_quotes(self):
        template = Template("{% load form_tags %}{% text_field form.field label=\"Friend's Email\" %}")
        request = HttpRequest()
        form = TestForm()
        content = template.render(Context(dict(form=form, request=request)))
        self.assert_("Friend&#39;s Email" in content)

    def test_display_text_field_ignore_non_kwargs(self):
        template = Template('{% load form_tags %}{% text_field form.field "Some arg" %}')
        request = HttpRequest()
        form = TestForm()
        content = template.render(Context(dict(form=form, request=request)))
        self.assert_("input" in content)

    def test_define_template_from_context(self):
        template = Template("{% load form_tags %}{% with 'gfaforms/_mobile_text_field.html' as text_field_template %}{% text_field form.field placeholder='Test' %}{% endwith %}")
        request = HttpRequest()
        form = TestForm()
        self.assert_('input' in \
            template.render(Context(dict(form=form, request=request))))
        self.assert_('label' not in \
            template.render(Context(dict(form=form, request=request))))

    def test_no_form(self):
        template = Template("{% load form_tags %}{% text_field form.field %}")
        request = HttpRequest()
        self.assertEqual(template.render(Context(dict(request=request))), "")
