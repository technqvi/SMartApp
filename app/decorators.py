from django.http import HttpResponse
from django.shortcuts import redirect
from app.models import *


def manger_and_viewer_engineer_only(view_func):
	def wrapper_function(request, *args, **kwargs):
	

	  is_in_manager_group = Manager.objects.filter(user=request.user).exists()
	  is_in_engineer_group = Engineer.objects.filter(user=request.user).exists()

	  if   is_in_manager_group or is_in_engineer_group:
		  return view_func(request, *args, **kwargs)
	  else:
		  return HttpResponse(f'<h2>You are not authorized to access this web application.</h2><b>Contact administrator to add this user to the manager OR engineer table in database</b>')

	return wrapper_function

def manger_and_viewer_only(view_func):
	def wrapper_function(request, *args, **kwargs):

	  is_in_manager_group = Manager.objects.filter(user=request.user).exists()
	  if   is_in_manager_group:
		  return view_func(request, *args, **kwargs)
	  else:
		  return HttpResponse('<h2>You are not authorized to access this web application.</h2><b>Contact administrator to add this user to the manager table in database</b>')

	return wrapper_function

def manger_only(view_func):
	def wrapper_function(request, *args, **kwargs):

	  is_in_manager_group = Manager.objects.filter(user=request.user,is_site_manager__exact=True).exists()
	  if   is_in_manager_group:
		  return view_func(request, *args, **kwargs)
	  else:
		  return HttpResponse('<h2>You are not authorized to access this page.</h2><b>This page is for only site manager</b>')

	return wrapper_function

def staff_admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
	  if   request.user.is_staff:
		  return view_func(request, *args, **kwargs)
	  else:
		  return HttpResponse('<h2>Allow only Staff-Admin to access this page.</h2><b>This page is for only staff admin  to import model</b>')

	return wrapper_function



def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func


def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator

def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):

		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'site-manager':
			return redirect('user-page')

		if group == 'administrator':
			return view_func(request, *args, **kwargs)

	return wrapper_function




