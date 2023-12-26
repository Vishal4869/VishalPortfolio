from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('main')
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
				return redirect('main')
		return wrapper_func
	return decorator

def apply_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.candidates.applicant_name:
			return view_func(request, *args, **kwargs)
		else:
			return redirect('caccount')

	return wrapper_func

def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'customer':
			return redirect('user-page')

		if group == 'admin':
			return view_func(request, *args, **kwargs)

	return wrapper_function


def home_page(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'Hr':
			return redirect('recruiterPage')

		if group == 'jobseeker':
			return redirect('candidatePage')

		else :
			return view_func(request, *args, **kwargs)

	return wrapper_function

def login_page(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'Hr':
			return redirect('recruiterLogin')

		if group == 'jobseeker':
			return redirect('candidateLogin')

		else :
			return redirect('registerPage')
	return wrapper_function
