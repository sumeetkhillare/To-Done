from django.urls import path
from . import views

app_name = "todo"


# Urls for to-done app
urlpatterns = [
    path('', views.index, name='index'),
    path('upload-voice-note/<int:list_item_id>/', views.upload_voice_note, name='upload_voice_note'),
    path('voice-notes/', views.voice_notes_view, name='voice_notes'),
    path('todo', views.index, name='todo'),
    path('todo/<int:list_id>', views.index, name='todo_list_id'),
    path('todo/new-from-template', views.todo_from_template, name='todo_from_template'),
    path('delete-todo', views.delete_todo, name='delete_todo'),
    path('templates', views.template, name='template'),
    path('templates/<int:template_id>', views.template, name='template'),
    path('templates/new-from-todo', views.template_from_todo, name='template_from_todo'),
    path('updateListItem', views.updateListItem, name='updateListItem'),
    path('updateListItemIn', views.updateListItemIn, name='updateListItemIn'),
    path('removeListItem', views.removeListItem, name='removeListItem'),
    path('createNewTodoList', views.createNewTodoList, name='createNewTodoList'),
    path('getListItemByName', views.getListItemByName, name='getListItemByName'),
    path('getListItemById', views.getListItemById, name='getListItemById'),
    path('markListItem', views.markListItem, name='markListItem'),
    path('addNewListItem', views.addNewListItem, name='addNewListItem'),
    path('updateListItem/<int:item_id>', views.updateListItem, name='updateListItem'),
    path('updateListItemIn/<int:item_id>', views.updateListItemIn, name='updateListItemIn'),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('auth_receiver', views.auth_receiver, name='auth_receiver'),
    path('kanban/', views.kanban_view, name='kanban'),
    path('kanban/add/', views.add_task, name='add_task'),
    path('kanban/update/<int:task_id>/', views.update_task, name='update_task'),
    path('kanban/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('update-task-status/', views.update_task_status, name='update_task_status'),
    path('update-template-item/<int:item_id>', views.update_template_item, name='update_template_item'),
    path('delete-template-item/<int:item_id>', views.delete_template_item, name='delete_template_item'),
    path('delete-template', views.delete_template, name='delete_template'),
]
