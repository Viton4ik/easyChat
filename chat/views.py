from django.shortcuts import render, get_object_or_404, redirect

from .models import Chat, UserProfile
from django.contrib.auth.models import User

import os

from django.conf import settings

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404

# rest_framework
import json
from rest_framework import viewsets
from rest_framework import permissions            
# https://www.django-rest-framework.org/api-guide/permissions/

import django_filters.rest_framework
from chat.serializers import *

from django.contrib.auth.decorators import login_required

# another way to create room (is not been used)
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
    permission_classes = [permissions.IsAuthenticated]


class MessageViewset(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filterset_fields = ['id', 'user', 'chat', 'content', 'createTime', ]

    # set a readOnly by default using rest_framework
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, pk, format=None): # set new functionality for delete
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Message(status=204) #status.HTTP_204_NO_CONTENT


class UserProfileSerializer(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    # set a IsAuthenticated rights by default using rest_framework
    permission_classes = [permissions.IsAuthenticated]

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['id', 'username', 'first_name', 'last_name', 'email', ]

    # set a IsAdminUser rights by default using rest_framework
    # permission_classes = [permissions.IsAdminUser]
    # set a readOnly
    # permission_classes = [permissions.IsAuthenticated|ReadOnly]
    permission_classes = [permissions.IsAuthenticated]

# ==========================


# ===== REST API ===== 
# is not used
def getChats(_):
    rooms = Chat.objects.all().values(
        'id',
        'name',
    )
    rooms_list = list(rooms)
    rooms_json = json.dumps(rooms_list)
    return HttpResponse(content=rooms_json, status=200, content_type='application/json')

# is not used
def getChat(_, pk):
    rooms = Chat.objects.filter(pk=pk).values(
        'id',
        'name',
        'users',
        )
    return HttpResponse(content=rooms, status=200)

# is not used
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

# is not used
def deleteMessage(_, pk):
    message_ = str(Message.objects.get(pk=pk))
    message = Message.objects.get(pk=pk).delete()

    return HttpResponseRedirect('../chats/')

def deleteChat(_, pk):
    Chat.objects.get(pk=pk).delete()

    return HttpResponseRedirect('../chats/')
# ====================


# ===== views =====
def html_404(request):
    return render(request, '404.html', {
        }, status=404)

@login_required
def getRooms(request):
    roomWithIds=Chat.objects.filter().values('id', "name",)
    rooms = Chat.objects.all()
    user = request.user
    print('user:', user)
    print('user.id:', user.id)

    try:
        userProfile = UserProfile.objects.get(user=user)
        avatar = userProfile.avatar.url
    except:
        avatar = '/media/avatars/default.png'

    avatar_full_url = settings.SITE_URL + avatar
    print('avatar_full_url:', avatar_full_url)

    return render(request, 'chat/rooms.html', {'rooms': rooms, 'roomWithIds': roomWithIds, 'user' : user, 'avatar' : avatar, 'avatar_full_url' : avatar_full_url, })

@login_required
def getRoom(request, pk):
    room = Chat.objects.get(pk=pk)

    QuerySetUsers = User.objects.filter(chats=pk).values('username', 'id')
    users = list(QuerySetUsers)
    
    try:
        userProfile = UserProfile.objects.get(user=request.user)
        avatar = userProfile.avatar.url
    except:
        avatar = '/media/avatars/default.png'

    messages = Message.objects.filter(chat=room)

    return render(request, 'chat/room.html', {'room': room, 'users' : users, 'avatar' : avatar, 'messages' : messages, })

@login_required
def userAccount(request, pk):
    try:
        userPk = User.objects.get(id=pk)
        userProfile = UserProfile.objects.get(user=pk)
    except User.DoesNotExist:
        return HttpResponseRedirect('../404/') 
     
    try:
        avatar = userProfile.avatar.url
    except:
        avatar = '/media/avatars/default.png'

    # to hide buttons for others users
    isRequestUser = True if request.user.id == pk else False  

    if request.method == 'POST' and request.FILES['avatar']:
        # save file in 'media' folder
        file = request.FILES['avatar']
        filename = file.name
        with open(os.path.join('media/avatars/', filename), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        # set new avatar in DB
        userProfile.avatar = f'avatars/{file.name}'
        userProfile.save()

    return render(request, 'chat/user.html', {'avatar': avatar, 'userPk': userPk, "userProfile": userProfile, 'isRequestUser': isRequestUser})

