from django.db import models
from django.contrib.auth.models import User

class List(models.Model):
    title_text = models.CharField(max_length=100, db_index=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    list_tag = models.CharField(max_length=50, default='none')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_shared = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.title_text

class ListTags(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tag_name = models.CharField(max_length=50, null=True, blank=True)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.tag_name


class ListItem(models.Model):
    # the name of a list item
    item_name = models.CharField(max_length=50, null=True, blank=True)
    # the text note of a list item
    item_text = models.CharField(max_length=100)
    status = models.CharField(max_length=10, null=True)
    is_done = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='list')
    finished_on = models.DateTimeField()
    due_date = models.DateField()
    tag_color = models.CharField(max_length=10)

    def __str__(self):
        return "%s: %s" % (str(self.item_text), self.is_done)


class Template(models.Model):
    title_text = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "%s" % self.title_text


class TemplateItem(models.Model):
    item_text = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now=True)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    finished_on = models.DateTimeField()
    due_date = models.DateField()
    tag_color = models.CharField(max_length=10)

    def __str__(self):
        return "%s" % self.item_text

class SharedUsers(models.Model):
    list_id = models.ForeignKey(List, on_delete=models.CASCADE)
    shared_user = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % str(self.list_id)

class SharedList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shared_list_id = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % str(self.user)

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title