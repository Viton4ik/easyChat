from django.urls import path

from .views import logout_view, signup# SignUp

from django.contrib.auth.views import LoginView


urlpatterns = [
    # path('signup/', SignUp.as_view(), name='signup'),
    path('signup/', signup, name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

]