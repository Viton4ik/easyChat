from django.shortcuts import render

from .models import Chat
from django.contrib.auth.models import User

from pprint import pprint

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed

# from django.urls import reverse

# rest_framework
import json
from rest_framework import viewsets
from rest_framework import permissions            # https://www.django-rest-framework.org/api-guide/permissions/
# from rest_framework.response import Response
import django_filters.rest_framework
from chat.serializers import *
# from chat.models import *


# ===== rest_framework =====

# create a ReadOnly
class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class ChatViewset(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["id", "name", "users",]
    
    # deny all by default using rest_framework 
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MessageViewset(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filterset_fields = ['id', 'user', 'chat', 'content', 'createTime', ]

    # set a readOnly by default using rest_framework
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def destroy(self, request, pk, format=None): # set new functionality for delete
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Message(status=204) #status.HTTP_204_NO_CONTENT


class UserProfileSerializer(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    # set a IsAuthenticated rights by default using rest_framework
    # permission_classes = [permissions.IsAuthenticated]

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['id', 'username', 'first_name', 'last_name', 'email', ]

    # set a IsAdminUser rights by default using rest_framework
    # permission_classes = [permissions.IsAdminUser]
    # set a readOnly
    # permission_classes = [permissions.IsAuthenticated|ReadOnly]

# ==========================


# ===== REST API =====
def getChats(_):
    rooms = Chat.objects.all().values(
        'id',
        'name',
        # 'users',
        )
    return HttpResponse(content=rooms, status=200)

def getChat(_, pk):
    rooms = Chat.objects.filter(pk=pk).values(
        'id',
        'name',
        'users',
        )
    return HttpResponse(content=rooms, status=200)

def getMessages(_):
    messages = Message.objects.all().values(
        'id',
        'chat',
        'user',
        'content',
        'createTime',
        )
    return HttpResponse(content=messages, status=200)

def getMessage(_, pk):
    message = Message.objects.filter(pk=pk).values(
        'id',
        'chat',
        'user',
        'content',
        'createTime',
        )
    return HttpResponse(content=message, status=200)

def createRoom(request):
    if request.method == 'POST':
    # body = json.loads(request.body.decode('utf-8'))
        body = json.loads(request.body)
        newRoom = Chat.objects.create(
            name=body['name'],
            users=body['users'],
            )
        return JsonResponse({'room_id': newRoom.id}, status=201)
    else:
        # return HttpResponseNotAllowed(['POST'])
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def createMessage(request):
    if request.method == 'POST':
    # body = json.loads(request.body.decode('utf-8'))
        body = json.loads(request.body)
        newMessage = Message.objects.create(
            chat=body['chat'],
            user=body['user'],
            content=body['content'], 
            )
        return HttpResponse(content=newMessage, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def editRoom(request, pk):
    body = json.loads(request.body)
    room = Chat.objects.get(pk=pk)
    for attr, value in body.items():
        setattr(room, attr, value)
    room.save()
    data = {'name': room.name, 'users': room.users,}
    return JsonResponse({'data': data}, status=200)

def editMessage(request, pk):
    body = json.loads(request.body)
    message = Message.objects.get(pk=pk)
    for attr, value in body.items():
        setattr(message, attr, value)
    message.save()
    data = {'chat': message.chat, 'user': message.user, 'content': message.content,}
    return JsonResponse({'data': data}, status=200)

def deleteMessage(_, pk):
    message_ = str(Message.objects.get(pk=pk))
    message = Message.objects.get(pk=pk).delete()

    return HttpResponseRedirect('../messages/')

def deleteChat(_, pk):
    Chat.objects.get(pk=pk).delete()

    return HttpResponseRedirect('../chats/')



# ====================

def getRooms(request):
    roomWithIds=Chat.objects.filter().values('id', "name",)
    rooms = Chat.objects.all()

    return render(request, 'chat/rooms.html', {'rooms': rooms, 'roomWithIds': roomWithIds, })


def getRoom(request, pk):
    room = Chat.objects.get(pk=pk)

    QuerySetUsers = User.objects.filter(chats=pk).values_list('username', flat=True)
    users = list(QuerySetUsers)

    return render(request, 'chat/room.html', {'room': room, 'users' : users})
