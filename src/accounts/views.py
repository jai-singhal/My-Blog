from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout,
	)
from .forms import UserLoginForm, UserRegisterForm

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect



def login_view(request):
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username = username, password = password)
		login(request, user)
		return redirect("/")
	return render(request, "accounts_form.html", {
		"title" : "Login",
		"forms" : form,
	})


def register_view(request):
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save()
		password = form.cleaned_data.get("password")	
		user.set_password(password)
		user.save()
		new_user = authenticate(username = user.username, password = password)
		login(request, new_user)
		return HttpResponseRedirect("/confirm_email")
	return render(request, "accounts_form.html", {
		"title" : "Register",
		"forms" : form,
	})


def logout_view(request):
	logout(request)
	return HttpResponseRedirect("/")