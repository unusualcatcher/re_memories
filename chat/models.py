from django.db import models
from django.contrib.auth.models import User

class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique=True)
    member1 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='chatgroup_member1')
    member2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='chatgroup_member2')

    def __str__(self) -> str:
        return self.group_name

class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=600)
    created = models.DateTimeField()

    def __str__(self) -> str:
        return f'{self.author.username}: {self.body}'
    
    class Meta:
        ordering = ['-created']
