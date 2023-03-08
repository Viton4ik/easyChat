
from .views import Chat, getRooms, getRoom, getChats, getMessage, createMessage, createRoom, editRoom, editMessage, deleteMessage, getMessages, getChat, deleteChat

from django.urls import path

# rest_framework
from django.urls import path, include
from rest_framework import routers
from chat import views
router = routers.DefaultRouter()
router.register(r'room', views.ChatViewset)
router.register(r'message', views.MessageViewset)
router.register(r'userProfile', views.UserProfileSerializer)
router.register(r'user', views.UserViewset)


urlpatterns = [

   path('rooms/', getRooms, name='getRooms'),
   path('rooms/<int:pk>', getRoom, name='getRoom'),

   # add REST API
   path('api/chats/', getChats),
   path('api/chats/<int:pk>', getChat),
   path('api/messages/<int:pk>', getMessage),
   path('api/messages/', getMessages, name='messages'),
   path('api/newRoom/', createRoom),
   path('api/newMessage/', createMessage),
   path('api/editRoom/<int:pk>', editRoom),
   path('api/editMessage/<int:pk>', editMessage),
   path('api/deleteMessage/<int:pk>', deleteMessage),
   path('api/deleteChat/<int:pk>', deleteChat),

   # rest_framework_routers
   #  path('', include(router.urls)),
   #  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
   path('api-auth/', include(router.urls), name='api'),

]