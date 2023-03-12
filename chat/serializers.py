
from .models import *
from rest_framework import serializers

class ChatSerializer(serializers.HyperlinkedModelSerializer):
# class ChatSerializer(serializers.ModelSerializer):
   class Meta:
       model = Chat
       fields = ['id', 'name', 'users',]


class MessageSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Message
       fields = ['id', 'user', 'chat', 'content', 'createTime', ]
    #    depth = 1


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = UserProfile
       fields = ['id', 'user', 'avatar',]


class UserSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = User
       fields = ['id', 'username', 'first_name', 'last_name', 'email', 'url', "chats"] #'is_superuser', 
    
