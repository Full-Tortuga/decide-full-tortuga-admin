from django.contrib import admin
from django.http.response import HttpResponseRedirect
from .models import TelegramBot
from .urls import urlpatterns

class TelegramBotAdmin(admin.ModelAdmin):
    list_display=('user_id', 'auto_msg')
    list_filter=('auto_msg',)
    ordering=('user_id', 'auto_msg')
    change_list_template = "visualizer/telegram_admin.html"

admin.site.register(TelegramBot, TelegramBotAdmin)