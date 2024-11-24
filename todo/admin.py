from django.contrib import admin

# Register your models here.
from .models import List, ListTags, ListItem, TemplateItem, SharedUsers, SharedList, Task

admin.site.register(List)
admin.site.register(ListTags)
admin.site.register(ListItem)
admin.site.register(TemplateItem)
admin.site.register(SharedUsers)
admin.site.register(SharedList)
admin.site.register(Task)