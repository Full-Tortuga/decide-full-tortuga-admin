from django.db import models

class TelegramBot(models.Model):
    user_id=models.BigIntegerField(primary_key=True)
    auto_msg=models.BooleanField(default=False)
    
    def __str__(self):
        return '{}'.format(self.auto_msg)
    
    class Meta:
        verbose_name = 'Telegram user'