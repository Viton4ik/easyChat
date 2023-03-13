from django.shortcuts import render

from .models import Chat
from django.contrib.auth.models import User

from pprint import pprint

from django.conf import settings

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed

# from django.urls import reverse

# rest_framework
import json
from rest_framework import viewsets
from rest_framework import permissions            # https://www.django-rest-framework.org/api-guide/permissions/
from rest_framework.response import Response
import django_filters.rest_framework
from chat.serializers import *


# another way to create room (usless now)
from rest_framework.generics import CreateAPIView
class ChatCreateView(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
#############################

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
# usles now
def getChats(_):
    rooms = Chat.objects.all().values(
        'id',
        'name',
    )
    # преобразовываем QuerySet в список словарей
    rooms_list = list(rooms)
    # преобразовываем список словарей в JSON-строку
    rooms_json = json.dumps(rooms_list)
    return HttpResponse(content=rooms_json, status=200, content_type='application/json')
# usles now
def getChat(_, pk):
    rooms = Chat.objects.filter(pk=pk).values(
        'id',
        'name',
        'users',
        )
    return HttpResponse(content=rooms, status=200)
# usles now
def getMessages(_):
    messages = Message.objects.all().values(
        'id',
        'chat',
        'user',
        'content',
        'createTime',
        )
    return HttpResponse(content=messages, status=200)
# usles now
def getMessage(_, pk):
    message = Message.objects.filter(pk=pk).values(
        'id',
        'chat',
        'user',
        'content',
        'createTime',
        )
    return HttpResponse(content=message, status=200)
# usles now
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
# usles now
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
# usles now
def editRoom(request, pk):
    # try:
    #     body = json.loads(request.body)
    # except json.JSONDecodeError as e:
    #     return JsonResponse({'error': 'Invalid JSON: {}'.format(str(e))}, status=400)


    body = json.loads(request.body.decode('utf-8'))
    
    room = Chat.objects.get(pk=pk)
    print(body)
    for attr, value in body.items():
        setattr(room, attr, value)
    room.save()
    data = {'name': room.name, 'users': room.users}
    return JsonResponse({'data': data}, status=200)

# from rest_framework import status
# from rest_framework.decorators import api_view

# @api_view(['PUT'])
# def editRoom(request, pk):
#     try:
#         chat = Chat.objects.get(pk=pk)
#     except Chat.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     serializer = ChatSerializer(chat, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# usles now
def editMessage(request, pk):
    body = json.loads(request.body)
    message = Message.objects.get(pk=pk)
    for attr, value in body.items():
        setattr(message, attr, value)
    message.save()
    data = {'chat': message.chat, 'user': message.user, 'content': message.content,}
    return JsonResponse({'data': data}, status=200)
# usles now
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
    user = request.user
    print('user:', user)
    print('user.id:', user.id)

    try:
        userProfile = UserProfile.objects.get(user=user)
        # print('avatar:', userProfile.avatar.url)
        avatar = userProfile.avatar.url
    except:
        avatar = '/media/avatars/default.png'

    avatar_full_url = settings.SITE_URL + avatar
    print('avatar_full_url:', avatar_full_url)

    return render(request, 'chat/rooms.html', {'rooms': rooms, 'roomWithIds': roomWithIds, 'user' : user, 'avatar' : avatar, 'avatar_full_url' : avatar_full_url, })



def getRoom(request, pk):
    room = Chat.objects.get(pk=pk)

    QuerySetUsers = User.objects.filter(chats=pk).values_list('username', flat=True)
    users = list(QuerySetUsers)
    
    try:
        userProfile = UserProfile.objects.get(user=request.user)
        avatar = userProfile.avatar.url
    except:
        avatar = '/media/avatars/default.png'

    return render(request, 'chat/room.html', {'room': room, 'users' : users, 'avatar' : avatar,})
