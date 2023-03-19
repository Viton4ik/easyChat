
from .views import getRooms, getRoom, getChats, createRoom, deleteMessage, getChat, deleteChat, userAccount, html_404

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

# another way to create room (is not been used)
# from .views import ChatCreateView

urlpatterns = [

   path('rooms/', getRooms, name='getRooms'),
   path('rooms/<int:pk>', getRoom, name='getRoom'),
   path('user/<int:pk>', userAccount, name='userAccount'),
   path('404/', html_404, name='html_404'),

   # add REST API
   path('api/chats/', getChats),
   path('api/chats/<int:pk>', getChat),
   path('api/newRoom/', createRoom),
   path('api/deleteMessage/<int:pk>', deleteMessage),
   path('api/deleteChat/<int:pk>', deleteChat),

   # another way to create room (is not been used)
   # path('chat/create/', ChatCreateView.as_view(), name='chat_create'), 

   # rest_framework_routers
   #  path('', include(router.urls)),
   #  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
   path('api-auth/', include(router.urls), name='api'),

]
