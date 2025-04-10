from django.shortcuts import render, redirect
from django.views import View


from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.models import User


class LoginView(View):
    '''Login view'''
    template_name = 'accounts/login.html'

    def get(self, request):
        '''Handles GET requests'''
        return render(request, self.template_name)

    def post(self, request):
        '''Handles POST requests'''
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # reset the login attempt
            messages.success(request, f'Welcome, {user.name.split(" ")[0].capitalize()}!')
            return redirect('dashboard:dashboard')
        else:
            messages.info(request, 'Invalid Username or Password')
            return render(request, self.template_name)
        

class LogoutView(View):
    '''Logout view'''
    def get(self, request):
        '''Handles GET requests'''
        logout(request)
        return redirect('dashboard:login')