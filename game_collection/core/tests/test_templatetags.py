from django.test import TestCase
from django import forms
from django.template import Template, Context

class MyForm(forms.Form):
    title = forms.CharField()

class GameTest(TestCase):
    def test_adds_class(self):
        context = Context({'form': MyForm()})
        template = Template('{% load addcss %} {{form.title|addcss:"my custom classes"}}')
        content = template.render(context)
        self.assertIn('class="my custom classes"', content)
