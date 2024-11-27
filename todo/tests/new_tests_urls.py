from django.test import SimpleTestCase
from django.urls import reverse, resolve
from todo.views import index,todo_from_template,template_from_todo, login,template

class TestURLS(SimpleTestCase):
    def test_index_url_resolves(self):
        url = reverse('todo:index')
        self.assertEqual(resolve(url).func, index)

    def test_todo_from_template_url_resolves(self):
        url = reverse('todo:todo_from_template')
        self.assertEqual(resolve(url).func, todo_from_template)

    def test_template_from_todo_url_resolves(self):
        url = reverse('todo:template_from_todo')
        self.assertEqual(resolve(url).func, template_from_todo)

    def test_template_url_resolves(self):
        url = reverse('todo:template')
        self.assertEqual(resolve(url).func, template)

    def test_template_with_id_url_resolves(self):
        url = reverse('todo:template', args=[1])
        self.assertEqual(resolve(url).func, template)


