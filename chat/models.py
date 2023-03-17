
from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    name = models.CharField(max_length=128)
    users = models.ManyToManyField(User, related_name='chats')

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    createTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} to {self.chat.name}: {self.content}'
    
    class Meta:
        ordering = ('createTime',)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

