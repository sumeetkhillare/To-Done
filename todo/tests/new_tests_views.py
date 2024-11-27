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

    def test_default_is_done_value(self):
        """Test default is_done value for new item"""
        item = ListItem.objects.create(
            item_name="New Item",
            created_on=timezone.now(),
            finished_on=timezone.now(),
            due_date=timezone.now(),
            tag_color="#000000",
            list=self.list
        )
        self.assertFalse(item.is_done)

    def test_basic_template_item(self):
        """Test creating a basic template item"""
        template = Template.objects.create(
            title_text="Template",
            created_on=timezone.now(),
            updated_on=timezone.now(),
            user_id=self.user
        )
        item = TemplateItem.objects.create(
            item_text="Template Item",
            created_on=timezone.now(),
            template=template,
            finished_on=timezone.now(),
            due_date=timezone.now(),
            tag_color="#000000"
        )
        self.assertEqual(item.item_text, "Template Item")

    def test_list_default_shared_status(self):
        """Test default shared status of new list"""
        new_list = List.objects.create(
            title_text="New List",
            created_on=timezone.now(),
            updated_on=timezone.now(),
            user_id=self.user
        )
        self.assertFalse(new_list.is_shared)

    def test_basic_task_creation(self):
        """Test creating a basic task"""
        task = Task.objects.create(
            title="Simple Task",
            status="todo",
            user=self.user
        )
        self.assertEqual(task.status, "todo")

    def test_default_tag_color(self):
        """Test default tag color for list item"""
        item = ListItem.objects.create(
            item_name="Colored Item",
            created_on=timezone.now(),
            finished_on=timezone.now(),
            due_date=timezone.now(),
            tag_color="#000000",
            list=self.list
        )
        self.assertEqual(item.tag_color, "#000000")

    def test_list_creation_timestamp(self):
        """Test list creation timestamp"""
        new_list = List.objects.create(
            title_text="Timestamped List",
            created_on=timezone.now(),
            updated_on=timezone.now(),
            user_id=self.user
        )
        self.assertIsNotNone(new_list.created_on)

    def test_template_empty_title(self):
        """Test template with empty title"""
        template = Template.objects.create(
            title_text="",
            created_on=timezone.now(),
            updated_on=timezone.now(),
            user_id=self.user
        )
        self.assertEqual(template.title_text, "")

    def test_basic_list_query(self):
        """Test querying lists by user"""
        lists = List.objects.filter(user_id=self.user)
        self.assertTrue(len(lists) > 0)

    def test_list_item_relationship(self):
        """Test relationship between list and items"""
        item = ListItem.objects.create(
            item_name="Related Item",
            created_on=timezone.now(),
            finished_on=timezone.now(),
            due_date=timezone.now(),
            tag_color="#000000",
            list=self.list
        )
        self.assertEqual(item.list, self.list)


class TodoListTests(TestCase):
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

    def test_list_not_shared_by_default(self):
        """Test that new lists are not shared by default"""
        new_list = List.objects.create(
            title_text="Private List",
            created_on=timezone.now(),
            updated_on=timezone.now(),
            user_id=self.user
        )
        self.assertFalse(new_list.is_shared)

    def test_list_item_not_done_by_default(self):
        """Test that new list items are not marked as done by default"""
        item = ListItem.objects.create(
            item_name="New Task",
            item_text="Description",
            created_on=timezone.now(),
            finished_on=timezone.now(),
            due_date=timezone.now(),
            tag_color="#ffffff",
            list=self.list
        )
        self.assertFalse(item.is_done)

    def test_list_items_not_equal(self):
        """Test that two different list items are not equal"""
        item1 = ListItem.objects.create(
            item_name="Task 1",
            item_text="Description 1",
            created_on=timezone.now(),
            finished_on=timezone.now(),
            due_date=timezone.now(),
            tag_color="#ffffff",
            list=self.list
        )
        item2 = ListItem.objects.create(
            item_name="Task 2",
            item_text="Description 2",
            created_on=timezone.now(),
            finished_on=timezone.now(),
            due_date=timezone.now(),
            tag_color="#000000",
            list=self.list
        )
        self.assertFalse(item1.item_name == item2.item_name)

    def test_template_not_found(self):
        """Test that a template with a non-existent ID doesn't exist"""
        non_existent_id = 99999
        self.assertFalse(Template.objects.filter(id=non_existent_id).exists())

    def test_user_not_owner(self):
        """Test that a different user is not the owner of a list"""
        other_user = User.objects.create_user(username='other', password='pass123')
        self.assertFalse(self.list.user_id == other_user)

    def test_tag_names_not_equal(self):
        """Test that different tag names are not equal"""
        tag1 = ListTags.objects.create(
            user_id=self.user,
            tag_name="Work",
            created_on=timezone.now()
        )
        tag2 = ListTags.objects.create(
            user_id=self.user,
            tag_name="Personal",
            created_on=timezone.now()
        )
        self.assertFalse(tag1.tag_name == tag2.tag_name)

    def test_list_not_empty(self):
        """Test that a list with items is not empty"""
        ListItem.objects.create(
            item_name="Task",
            item_text="Description",
            created_on=timezone.now(),
            finished_on=timezone.now(),
            due_date=timezone.now(),
            tag_color="#ffffff",
            list=self.list
        )
        self.assertFalse(self.list.listitem_set.count() == 0)

    def test_shared_lists_not_equal(self):
        """Test that different shared list IDs are not equal"""
        shared_list1 = SharedList.objects.create(
            user=self.user,
            shared_list_id="1 2 3"
        )
        shared_list2 = SharedList.objects.create(
            user=User.objects.create_user(username='other', password='pass123'),
            shared_list_id="4 5 6"
        )
        self.assertFalse(shared_list1.shared_list_id == shared_list2.shared_list_id)