from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.conf import settings
from appuser.models import AppUser
# Create your views here.

def login_view(request):

	mensaje = ''
	if request.user.is_authenticated:
		return redirect(reverse('appuser.home'))
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(username=username, password=password)

			if user:
				if user.is_active:
					login(request, user)
					return redirect(reverse('appuser.home'))
				else:
					mensaje = 'the user ' + username + ' is not active, plase' + \
					'consult with the system administrator'

			else:
				# el usuario no existe
				mensaje = 'username or password incorrect'

	return render(request, 'appuser/login.html', {'mensaje': mensaje})

def logout_view(request):
	logout(request)
	return redirect(reverse('appuser.login'))

def home_view(request):
	username = request.user.username
	if request.user.is_authenticated:
		objUsuario = AppUser.objects.get(user__id=request.user.id)
		#import pdb; pdb.set_trace()
		return render(request,'appuser/home.html',
			{
				'username': username.capitalize()
			}
		) 
	else:
		return render(request,'appuser/login.html',{})