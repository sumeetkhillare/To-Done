from django.urls import reverse
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from todo.views import login_request, template_from_todo, template, delete_todo, index, getListTagsByUserid, removeListItem, addNewListItem, updateListItem, createNewTodoList, register_request, getListItemByName, getListItemById, markListItem, todo_from_template
from django.utils import timezone
from todo.models import List, ListItem, Template, TemplateItem, ListTags, SharedList, Task
from todo.forms import NewUserForm
from django.contrib.messages.storage.fallback import FallbackStorage
from unittest.mock import patch
import json

class AdditionalViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='123')
        self.client.login(username='testuser', password='123')

    def test_register_request_valid_data(self):
        response = self.client.post(reverse('todo:register'), {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': '123',
            'password2': '123'
        })
        self.assertEqual(response.status_code, 200)

    def test_password_reset_request_valid_email(self):
        response = self.client.post(reverse('todo:password_reset'), {
            'email': 'testuser@test.com'
        })
        self.assertEqual(response.status_code, 200)

    def test_template_item_update(self):
        template_obj = Template.objects.create(
            title_text="Test Template",
            created_on=timezone.now(),
            updated_on=timezone.now(),
            user_id=self.user
        )
        template_item = TemplateItem.objects.create(
            item_text="Test Item",
            created_on=timezone.now(),
            template=template_obj,
            finished_on=timezone.now(),
            due_date=timezone.now(),
            tag_color="#ffffff"
        )
        data = {
            'item_text': 'Updated Item',
            'tag_color': '#000000'
        }
        response = self.client.post(
            reverse('todo:update_template_item', args=[template_item.id]),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_template_creation(self):
        response = self.client.post(reverse('todo:template_from_todo'), {
            'todo': 999  # Non-existent todo ID
        })
        self.assertEqual(response.status_code, 404)


class SimpleTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        self.list = List.objects.create(
            title_text="Test List",
            created_on=timezone.now(),
            updated_on=timezone.now(),
            user_id=self.user
        )

    def test_create_basic_list(self):
        """Test creating a basic list"""
        list_obj = List.objects.create(
            title_text="Simple List",
            created_on=timezone.now(),
            updated_on=timezone.now(),
            user_id=self.user
        )
        self.assertEqual(list_obj.title_text, "Simple List")

    def test_create_basic_list_item(self):
        """Test creating a basic list item"""
        item = ListItem.objects.create(
            item_name="Simple Item",
            created_on=timezone.now(),
            finished_on=timezone.now(),
            due_date=timezone.now(),
            tag_color="#000000",
            list=self.list
        )
        self.assertEqual(item.item_name, "Simple Item")

    def test_mark_item_as_done(self):
        """Test marking an item as done"""
        item = ListItem.objects.create(
            item_name="Test Item",
            created_on=timezone.now(),
            finished_on=timezone.now(),
            due_date=timezone.now(),
            tag_color="#000000",
            list=self.list
        )
        item.is_done = True
        item.save()
        self.assertTrue(item.is_done)

    def test_create_basic_template(self):
        """Test creating a basic template"""
        template = Template.objects.create(
            title_text="Basic Template",
            created_on=timezone.now(),
            updated_on=timezone.now(),
            user_id=self.user
        )
        self.assertEqual(template.title_text, "Basic Template")

    def test_create_list_tag(self):
        """Test creating a list tag"""
        tag = ListTags.objects.create(
            user_id=self.user,
            tag_name="Work",
            created_on=timezone.now()
        )
        self.assertEqual(tag.tag_name, "Work")

    def test_delete_list(self):
        """Test deleting a list"""
        list_count = List.objects.count()
        self.list.delete()
        self.assertEqual(List.objects.count(), list_count - 1)

    def test_update_list_title(self):
        """Test updating list title"""
        self.list.title_text = "Updated Title"
        self.list.save()
        self.assertEqual(self.list.title_text, "Updated Title")

    def test_create_shared_list(self):
        """Test creating a shared list"""
        shared_list = SharedList.objects.create(
            user=self.user,
            shared_list_id="1 2 3"
        )
        self.assertEqual(shared_list.shared_list_id, "1 2 3")

    def test_empty_list_item_text(self):
        """Test creating list item with empty text"""
        item = ListItem.objects.create(
            item_name="Empty Text Item",
            item_text="",
            created_on=timezone.now(),
            finished_on=timezone.now(),
            due_date=timezone.now(),
            tag_color="#000000",
            list=self.list
        )
        self.assertEqual(item.item_text, "")

    def test_list_tag_empty_name(self):
        """Test creating tag with empty name"""
        tag = ListTags.objects.create(
            user_id=self.user,
            tag_name="",
            created_on=timezone.now()
        )
        self.assertEqual(tag.tag_name, "")

    def test_today_due_date(self):
        """Test creating item with today's due date"""
        today = timezone.now().date()
        item = ListItem.objects.create(
            item_name="Today's Task",
            created_on=timezone.now(),
            finished_on=timezone.now(),
            due_date=today,
            tag_color="#000000",
            list=self.list
        )
        self.assertEqual(item.due_date, today)
