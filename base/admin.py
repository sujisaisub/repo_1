from django.contrib import admin
from base.models import ToDoList, Item, Feedback, ChatBotModel

# Register your models here.
admin.site.register(ToDoList)

admin.site.register(Item)

admin.site.register(Feedback)

admin.site.register(ChatBotModel)