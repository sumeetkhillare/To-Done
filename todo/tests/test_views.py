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


class TestViews(TestCase):
    def setUp(self):
        # Every test needs access to the client and request factory.
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def testLogin(self):
        request = self.factory.get('/login/')
        request.user = self.user
        post = request.POST.copy()  # to make it mutable
        post['todo'] = 1
        print(request)
        request.POST = post
        response = login_request(request)
        self.assertEqual(response.status_code, 200)

    def testSavingTodoList(self):
        response = self.client.get(reverse('todo:createNewTodoList'))
        self.assertEqual(response.status_code, 302)
        # print(response)

    def test_delete_todo_list(self):
        request = self.factory.get('/todo/')
        request.user = self.user
        todo = List.objects.create(
            title_text="test list",
            created_on=timezone.now(),
            updated_on=timezone.now(),
            user_id_id=self.user.id,
        )
        ListItem.objects.create(
            item_name="test item",
            item_text="This is a test item on a test list",
            created_on=timezone.now(),
            finished_on=timezone.now(),
            tag_color="#f9f9f9",
            due_date=timezone.now(),
            list=todo,
            is_done=False,
        )
        post = request.POST.copy()
        post['todo'] = 1
        request.POST = post
        response = delete_todo(request)
        self.assertEqual(response.status_code, 302)

    def test_getListTagsByUserid(self):
        request = self.factory.get('/todo/')
        request.user = self.user
        ListTags.objects.create(
            user_id_id = self.user.id,
            tag_name = 'test',
            created_on = timezone.now()
        )
        post = request.POST.copy()
        post['todo'] = 1
        request.POST = post
        request.method = "POST"
        response = getListTagsByUserid(request)
        print('response:')
        print(response)
        self.assertIsNotNone(response)

    def test_index(self):
        request = self.factory.get('/todo/')
        request.user = self.user
        response = index(request)
        self.assertEqual(response.status_code, 200)

    def test_template_from_todo_redirect(self):
        client = self.client
        response = client.get(reverse('todo:template_from_todo'))
        self.assertEquals(response.status_code, 302)

    def test_template_from_todo_function(self):
        request = self.factory.get('/todo/')
        request.user = self.user
        todo = List.objects.create(
            title_text="test list",
            created_on=timezone.now(),
            updated_on=timezone.now(),
            user_id_id=request.user.id,
        )
        item = ListItem.objects.create(
            item_name="test item",
            item_text="This is a test item on a test list",
            created_on=timezone.now(),
            finished_on=timezone.now(),
            tag_color="#f9f9f9",
            due_date=timezone.now(),
            list=todo,
            is_done=True,
        )
        post = request.POST.copy()  # to make it mutable
        post['todo'] = 1
        request.POST = post
        response = template_from_todo(request)
        self.assertEqual(response.status_code, 302)

    def test_template_display(self):
        request = self.factory.get('/todo/')
        request.user = self.user
        new_template = Template.objects.create(
            title_text="test template",
            created_on=timezone.now(),
            updated_on=timezone.now(),
            user_id_id=request.user.id
        )
        template_item = TemplateItem.objects.create(
            item_text="test item",
            created_on=timezone.now(),
            template=new_template,
            finished_on=timezone.now(),
            tag_color="#f9f9f9",
            due_date=timezone.now()
        )
        post = request.POST.copy()  # to make it mutable
        post['todo'] = 1
        request.POST = post
        response = template(request, 1)
        self.assertEqual(response.status_code, 200)
        
    def test_removeListItem(self):
        request = self.factory.get('/todo/')
        request.user = self.user

        todo = List.objects.create(
        title_text="test list",
        created_on=timezone.now(),
        updated_on=timezone.now(),
        user_id_id=self.user.id,
        )

        ListItem.objects.create(
            item_name="test item",
            item_text="This is a test item on a test list",
            created_on=timezone.now(),
            finished_on=timezone.now(),
            tag_color="#f9f9f9",
            due_date=timezone.now(),
            list=todo,
            is_done=False,
        )

        post = request.POST.copy()
        # post['list_item_id'] = 1
        request.method = "POST"
        request._body = json.dumps({ "list_item_id": 1 }).encode('utf-8')
        response = removeListItem(request)
        print(response)
        self.assertIsNotNone(response)
        
        
    def test_NewUserForm(self):
        form_data = { 'email': '123@123.com', 'username': '123', 'password1': 'K!35EGL&g7#U', 'password2': 'K!35EGL&g7#U'}
        form = NewUserForm(form_data)
        self.assertTrue(form.is_valid())
        
    def test_addNewListItem(self):

        todo = List.objects.create(
        title_text="test list",
        created_on=timezone.now(),
        updated_on=timezone.now(),
        user_id_id=self.user.id,
        )

        params = { 
            'list_id': todo.id,
            'list_item_name': "random", 
            "create_on": 1670292391,
            "due_date": "2023-01-01",
            "tag_color": "#f9f9f9",
            "item_text": "",
            "is_done": False
            }

        request = self.factory.post(f'/todo/', data=params, 
                                content_type="application/json")
        request.user = self.user
        # request.method = "POST"
        print(type(params))
        # param = json.dumps(param,cls=DateTimeEncoder)
        # request._body = json.dumps(params, separators=(',', ':')).encode('utf-8')
        temp = addNewListItem(request)
        response = index(request)
        self.assertEqual(response.status_code, 200)
        
    def test_updateListItem(self):
        request = self.factory.get('/todo/')
        request.user = self.user
        todo = List.objects.create(
            title_text="test list 2",
            created_on=timezone.now(),
            updated_on=timezone.now(),
            user_id_id=request.user.id,
        )
        item = ListItem.objects.create(
            item_name="test item 2",
            item_text="This is a test item on a test list",
            created_on=timezone.now(),
            finished_on=timezone.now(),
            tag_color="#f9f9f9",
            due_date=timezone.now(),
            list=todo,
            is_done=False,
        )
        post = request.POST.copy()
        post['todo'] = 1
        post['note'] = 'test note'
        request.POST = post
        request.method = "POST"
        response = updateListItem(request, item.id)
        self.assertEqual(response.status_code, 302)
        
    def test_createNewTodoList(self):
        test_data = {'list_name' : 'test',
                     'create_on' : 1670292391,
                     'list_tag' : 'test_tag',
                     'shared_user' : None,
                     'create_new_tag' : True}
        request = self.factory.post(f'/todo/', data=test_data, 
                                content_type="application/json")
        request.user = self.user
        temp = createNewTodoList(request)
        response = index(request)
        self.assertEqual(response.status_code, 200)
        
    def test_getListItemByName(self):
        todo = List.objects.create(
            title_text="test list",
            created_on=timezone.now(),
            updated_on=timezone.now(),
            user_id_id=self.user.id,
        )
        ListItem.objects.create(
            item_name="test item",
            item_text="This is a test item on a test list",
            created_on=timezone.now(),
            finished_on=timezone.now(),
            tag_color="#f9f9f9",
            due_date=timezone.now(),
            list=todo,
            is_done=False,
        )
        test_data = {'list_id' : '1',
                     'list_item_name' : "test item"
                     }
        request = self.factory.post(f'/todo/', data=test_data,
                                content_type="application/json")
        request.user = self.user
        response = getListItemByName(request)
        self.assertEqual(response.status_code, 200)
    
    def test_getListItemById(self):
        todo = List.objects.create(
            title_text="test list 3",
            created_on=timezone.now(),
            updated_on=timezone.now(),
            user_id_id=self.user.id,
        )
        item = ListItem.objects.create(
            item_name="test item 3",
            item_text="This is a test item on a test list",
            created_on=timezone.now(),
            finished_on=timezone.now(),
            tag_color="#f9f9f9",
            due_date=timezone.now(),
            list=todo,
            is_done=False,
        )
        test_data = {'list_id' : str(todo.id),
                     'list_item_name': 'test item 3',
                     'list_item_id': str(item.id)
                     }
        request = self.factory.post(f'/todo/', data=test_data, 
                                content_type="application/json")
        request.user = self.user
        temp = getListItemById(request)
        response = index(request)
        self.assertEqual(response.status_code, 200)
        
    def test_markListItem(self):
        todo = List.objects.create(
            title_text="test list",
            created_on=timezone.now(),
            updated_on=timezone.now(),
            user_id_id=self.user.id,
        )

        listItem = ListItem.objects.create(
            item_name="test item",
            item_text="This is a test item on a test list",
            created_on=timezone.now(),
            finished_on=timezone.now(),
            tag_color="#f9f9f9",
            due_date=timezone.now(),
            list=todo,
            is_done=False,
        )

        params = { 
            'list_id': todo.id,
            'list_item_name': listItem.item_name, 
            "create_on": 1670292391,
            "due_date": "2023-01-01",
            "finish_on": 1670292392,
            "is_done": True,
            "list_item_id": listItem.id,
            }

        request = self.factory.post(f'/todo/', data=params, 
                                content_type="application/json")
        request.user = self.user
        temp = markListItem(request)
        response = index(request)
        self.assertEqual(response.status_code, 200)
    
    def test_createNewTodoList2(self):
        test_data = {'list_name' : 'test',
                     'create_on' : 1670292391,
                     'list_tag' : 'test_tag',
                     'shared_user' : 'someone',
                     'create_new_tag' : True}
        request = self.factory.post(f'/todo/', data=test_data, 
                                content_type="application/json")
        request.user = self.user
        temp = createNewTodoList(request)
        response = index(request)
        self.assertEqual(response.status_code, 200)
    
    def test_createNewTodoList3(self):
        sharedUser = User.objects.create_user(
            username='share', email='share@…', password='top_secret')
        sharedList = SharedList.objects.create(
            user = sharedUser,
            shared_list_id = ""
        )
        
        test_data = {'list_name' : 'test',
                     'create_on' : 1670292391,
                     'list_tag' : 'test_tag',
                     'shared_user' : 'share',
                     'create_new_tag' : True}
        request = self.factory.post(f'/todo/', data=test_data, 
                                content_type="application/json")
        request.user = self.user
        temp = createNewTodoList(request)
        response = index(request)
        self.assertEqual(response.status_code, 200)
        
    def test_todo_from_template(self):
        request = self.factory.get('/todo/')
        request.user = self.user
        new_template = Template.objects.create(
            title_text="test template",
            created_on=timezone.now(),
            updated_on=timezone.now(),
            user_id_id=request.user.id
        )
        template_item = TemplateItem.objects.create(
            item_text="test item",
            created_on=timezone.now(),
            template=new_template,
            finished_on=timezone.now(),
            tag_color="#f9f9f9",
            due_date=timezone.now()
        )
        
        post = request.POST.copy()
        post['todo'] = 1
        post['template'] = new_template.id
        request.POST = post
        request.method = "POST"
        response = todo_from_template(request)
        self.assertEqual(response.status_code, 302)

    def test_login_request(self):
        test_data = {'username' : 'jacob',
                     'password' : 'top_secret'}
        request = self.factory.post(f'/login/', data=test_data, 
                                content_type="application/json")
        request.user = self.user
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = login_request(request)
        self.assertEqual(response.status_code, 200)

class ListModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.list = List.objects.create(
            title_text='My Todo List',
            created_on=timezone.now(),
            updated_on=timezone.now(),
            list_tag='personal',
            user_id=self.user,
            is_shared=False
        )

    def test_list_string_representation(self):
        self.assertEqual(str(self.list), 'My Todo List')

class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.task = Task.objects.create(
            title='My First Task',
            status='todo',
            user=self.user
        )

    def test_task_string_representation(self):
        self.assertEqual(str(self.task), 'My First Task')

class TestKanbanViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_kanban_view_authenticated(self):
        response = self.client.get('/kanban/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/kanban_dd.html')
        self.assertIn('tasks', response.context)

    def test_kanban_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get('/kanban/')
        self.assertRedirects(response, '/login')

    def test_add_task_authenticated(self):
        response = self.client.post('/kanban/add/', {'title': 'New Task'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ListItem.objects.count(), 0)
        self.assertEqual(ListItem.objects.first().item_name, 'New Task')

    def test_add_task_unauthenticated(self):
        self.client.logout()
        response = self.client.post('/kanban/add/', {'title': 'New Task'}, content_type='application/json')
        self.assertRedirects(response, '/login')

    def test_update_task_authenticated(self):
        List.objects.create(id=1, title_text='My First List', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        task = ListItem.objects.create(item_name='Task to Update', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        response = self.client.post(f'/kanban/update/{task.id}/', {'status': 'done'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.status, 'done')

    def test_update_task_unauthenticated(self):
        List.objects.create(id=1, title_text='My First List', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        task = ListItem.objects.create(item_name='Task to Update', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        self.client.logout()
        response = self.client.post(f'/kanban/update/{task.id}/', {'status': 'done'}, content_type='application/json')
        self.assertRedirects(response, '/login')

    def test_delete_task_authenticated(self):
        List.objects.create(id=1, title_text='My First List', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        task = ListItem.objects.create(item_name='Task to Delete', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        response = self.client.post(f'/kanban/delete/{task.id}/', content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(ListItem.objects.count(), 0)

    def test_delete_task_unauthenticated(self):
        List.objects.create(id=1, title_text='My First List', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        task = ListItem.objects.create(item_name='Task to Delete', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        self.client.logout()
        response = self.client.post(f'/kanban/delete/{task.id}/', content_type='application/json')
        self.assertRedirects(response, '/login')

    def test_update_task_status_authenticated(self):
        List.objects.create(id=1, title_text='My First List', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        task = ListItem.objects.create(item_name='Task for Status Update', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        data = json.dumps({'task_id': task.id, 'status': 'done'})
        response = self.client.post('/update-task-status/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertTrue(task.is_done)
        self.assertEqual(task.status, 'done')

    def test_update_task_status_invalid_task(self):
        data = json.dumps({'task_id': 999, 'status': 'done'})  # Non-existing task
        response = self.client.post('/update-task-status/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'error', 'message': 'Task not found.'})

    def test_update_task_status_invalid_request_method(self):
        response = self.client.get('/update-task-status/')

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_kanban_view_authenticated(self):
        response = self.client.get('/kanban/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/kanban_dd.html')
        self.assertIn('tasks', response.context)

    def test_kanban_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get('/kanban/')
        self.assertRedirects(response, '/login')

    def test_add_task_authenticated_with_special_chars(self):
        response = self.client.post('/kanban/add/', {'title': 'Task @ 2024!'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ListItem.objects.count(), 0)
        self.assertEqual(ListItem.objects.first().item_name, 'Task @ 2024!')

    def test_add_task_authenticated_with_empty_title(self):
        response = self.client.post('/kanban/add/', {'title': ''}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_add_task_authenticated_with_long_title(self):
        long_title = 'A' * 256  # Exceeding max_length
        response = self.client.post('/kanban/add/', {'title': long_title}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_add_task_authenticated_with_non_ascii(self):
        response = self.client.post('/kanban/add/', {'title': 'Tâsk with Accents'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ListItem.objects.count(), 0)
        self.assertEqual(ListItem.objects.first().item_name, 'Tâsk with Accents')

    def test_update_task_authenticated_with_different_status(self):
        List.objects.create(id=1, title_text='My First List', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        task = ListItem.objects.create(item_name='Task to Update', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        response = self.client.post(f'/kanban/update/{task.id}/', {'status': 'in_progress'}, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        task.refresh_from_db()
        self.assertEqual(task.status, 'in_progress')

    def test_update_task_authenticated_invalid_status(self):
        List.objects.create(id=1, title_text='My First List', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        task = ListItem.objects.create(item_name='Task to Update', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        response = self.client.post(f'/kanban/update/{task.id}/', {'status': 'invalid_status'}, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_update_task_status_authenticated_with_empty_task_id(self):
        data = json.dumps({'task_id': '1', 'status': 'done'})
        response = self.client.post('/update-task-status/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)  # Assuming empty ID is invalid

    def test_update_task_status_authenticated_with_invalid_task_id(self):
        data = json.dumps({'task_id': 999, 'status': 'done'})
        response = self.client.post('/update-task-status/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'error', 'message': 'Task not found.'})

    def test_delete_task_authenticated_with_non_existing_task(self):
        response = self.client.post('/kanban/delete/999/', content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_update_task_authenticated_with_no_status(self):
        List.objects.create(id=1, title_text='My First List', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        task = ListItem.objects.create(item_name='Task for Status Update', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        response = self.client.post(f'/kanban/update/{task.id}/', {'status': ''}, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_add_task_authenticated_with_json_format(self):
        data = json.dumps({'title': 'New JSON Task'})
        response = self.client.post('/kanban/add/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ListItem.objects.count(), 0)
        self.assertEqual(ListItem.objects.first().item_name, 'New JSON Task')

    def test_kanban_view_no_tasks(self):
        response = self.client.get('/kanban/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('tasks', response.context)
        self.assertEqual(len(response.context['tasks']), 0)

    def test_add_task_authenticated_with_missing_field(self):
        response = self.client.post('/kanban/add/', {'description': 'Missing title'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_update_task_authenticated_to_done(self):
        List.objects.create(id=1, title_text='My First List', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        task = ListItem.objects.create(item_name='Task for Update', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        response = self.client.post(f'/kanban/update/{task.id}/', {'status': 'done'}, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        task.refresh_from_db()
        self.assertTrue(task.is_done)

    def test_delete_task_authenticated_with_different_user(self):
        another_user = User.objects.create_user(username='anotheruser', password='anotherpassword')
        self.client.logout()
        self.client.login(username='anotheruser', password='anotherpassword')
        List.objects.create(id=1, title_text='My First List', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        task = ListItem.objects.create(item_name='Task to Delete', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        response = self.client.post(f'/kanban/delete/{task.id}/', content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_update_task_authenticated_with_future_due_date(self):
        future_due_date = timezone.now() + timezone.timedelta(days=30)
        List.objects.create(id=1, title_text='My First List', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        task = ListItem.objects.create(item_name='Task with Future Due Date', created_on=timezone.now(), finished_on=timezone.now(), due_date=future_due_date, tag_color="#ffffff", list_id=1)
        response = self.client.post(f'/kanban/update/{task.id}/', {'due_date': future_due_date}, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_update_task_authenticated_with_past_due_date(self):
        past_due_date = timezone.now() - timezone.timedelta(days=30)
        List.objects.create(id=1, title_text='My First List', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        task = ListItem.objects.create(item_name='Task with Past Due Date', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        response = self.client.post(f'/kanban/update/{task.id}/', {'due_date': past_due_date}, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    # def test_update_task_authenticated_with_nonexistent_list(self):
    #     task = ListItem.objects.create(item_name='Task for Nonexistent List', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=999)
    #     response = self.client.post(f'/kanban/update/{task.id}/', {'status': 'done'}, content_type='application/json')
    #     self.assertEqual(response.status_code, 404)  # Nonexistent list

    def test_delete_task_authenticated_without_permission(self):
        another_user = User.objects.create_user(username='anotheruser', password='anotherpassword')
        self.client.logout()
        self.client.login(username='anotheruser', password='anotherpassword')
        List.objects.create(id=1, title_text='My First List', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        task = ListItem.objects.create(item_name='Task to Delete', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        response = self.client.post(f'/kanban/delete/{task.id}/', content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_update_task_authenticated_with_invalid_task_data(self):
        List.objects.create(id=1, title_text='My First List', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        task = ListItem.objects.create(item_name='Task for Invalid Update', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        response = self.client.post(f'/kanban/update/{task.id}/', {'status': 'invalid_status'}, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_add_task_authenticated_with_special_characters_in_title(self):
        response = self.client.post('/kanban/add/', {'title': 'Special @#$%&* Characters'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ListItem.objects.count(), 0)
        self.assertEqual(ListItem.objects.first().item_name, 'Special @#$%&* Characters')

    def test_kanban_view_with_existing_tasks(self):
        List.objects.create(id=1, title_text='List with Tasks', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        ListItem.objects.create(item_name='Task 1', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        ListItem.objects.create(item_name='Task 2', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        response = self.client.get('/kanban/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 0)

    def test_add_task_authenticated_with_preexisting_title(self):
        List.objects.create(id=1, title_text='List with Duplicate Tasks', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        ListItem.objects.create(item_name='Duplicate Task', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        response = self.client.post('/kanban/add/', {'title': 'Duplicate Task'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_update_task_authenticated_with_large_data(self):
        large_data = 'A' * 10000  # Simulating a large data input
        List.objects.create(id=1, title_text='My First List', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        task = ListItem.objects.create(item_name='Large Task', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        response = self.client.post(f'/kanban/update/{task.id}/', {'item_text': large_data}, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_add_task_authenticated_with_list_tag(self):
        List.objects.create(id=1, title_text='List with Tag', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Work', is_shared=False)
        response = self.client.post('/kanban/add/', {'title': 'Task with Tag', 'list_tag': 'Work'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ListItem.objects.count(), 0)
        self.assertEqual(ListItem.objects.first().item_name, 'Task with Tag')

    def test_update_task_authenticated_with_task_color(self):
        List.objects.create(id=1, title_text='My First List', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        task = ListItem.objects.create(item_name='Task with Color', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        response = self.client.post(f'/kanban/update/{task.id}/', {'tag_color': '#ff0000'}, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        task.refresh_from_db()
        self.assertEqual(task.tag_color, '#ff0000')

    def test_kanban_view_authenticated_with_special_tag(self):
        List.objects.create(id=1, title_text='List with Special Tag', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Special & Unique', is_shared=False)
        response = self.client.get('/kanban/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('tasks', response.context)

    def test_add_task_authenticated_with_html_in_title(self):
        response = self.client.post('/kanban/add/', {'title': '<script>alert("XSS")</script>'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ListItem.objects.count(), 0)
        self.assertEqual(ListItem.objects.first().item_name, '<script>alert("XSS")</script>')

    def test_update_task_authenticated_with_xss_attempt(self):
        List.objects.create(id=1, title_text='My First List', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        task = ListItem.objects.create(item_name='Task with XSS', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        response = self.client.post(f'/kanban/update/{task.id}/', {'item_text': '<script>alert("XSS")</script>'}, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_delete_task_authenticated_with_success_message(self):
        List.objects.create(id=1, title_text='My First List', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        task = ListItem.objects.create(item_name='Task for Deletion', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        response = self.client.post(f'/kanban/delete/{task.id}/', content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {'status': 'success', 'message': 'Task deleted.'})

    def test_kanban_view_authenticated_with_no_tags(self):
        List.objects.create(id=1, title_text='List Without Tags', created_on=timezone.now(), updated_on=timezone.now(), list_tag='', is_shared=False)
        response = self.client.get('/kanban/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('tasks', response.context)

    def test_update_task_authenticated_with_empty_item_name(self):
        List.objects.create(id=1, title_text='My First List', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Default Tag', is_shared=False)
        task = ListItem.objects.create(item_name='Task with Name', created_on=timezone.now(), finished_on=timezone.now(), due_date=timezone.now(), tag_color="#ffffff", list_id=1)
        response = self.client.post(f'/kanban/update/{task.id}/', {'item_name': ''}, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_add_task_authenticated_with_tag_color(self):
        List.objects.create(id=1, title_text='List with Tag Color', created_on=timezone.now(), updated_on=timezone.now(), list_tag='Work', is_shared=False)
        response = self.client.post('/kanban/add/', {'title': 'Task with Color', 'tag_color': '#ff0000'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ListItem.objects.count(), 0)
        self.assertEqual(ListItem.objects.first().tag_color, '#ff0000')