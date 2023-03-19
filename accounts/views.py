from django.shortcuts import render, redirect

from django.contrib.auth import login
from django.contrib.auth import logout

from chat.models import UserProfile
# from django.contrib.auth.models import User

# from django.views.generic.edit import CreateView

from .forms import SignUpForm


# class SignUp(CreateView):
#     model = User
#     form_class = SignUpForm
#     success_url = '/login'
#     template_name = 'registration/signup.html'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('getRooms')
        
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})
    

def logout_view(request):
    logout(request)
    return redirect('login')