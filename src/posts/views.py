#import urllib.parse 
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from django.db.models import Q
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required

def post_list(request):
	queryset_list = Post.objects.active().order_by("-timestamp")
	if  request.user.is_staff or  request.user.is_superuser:
		queryset_list = Post.objects.all().order_by("-timestamp")
	
	query = request.GET.get("q")
	if query :
		queryset_list = queryset_list.filter(
			Q(title__icontains = query)|
			Q(content__icontains = query)|
			Q(user__first_name__icontains = query)|
			Q(user__last_name__icontains = query)
			).distinct()

	paginator = Paginator(queryset_list, 5) 
	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)
	date = datetime.now().date()
	context = {
		"object_list" : queryset,
		"title" : "List",
		"date" : date,
		"query" : query,
	}
	return render(request, "post_list.html", context)

@login_required(login_url='/login/')
def post_create(request):
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.user = request.user
		instance.save()
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form" : form,
		"type" : "Create",
	}
	
	return render(request, "post_form.html", context)


def post_detail(request, slug = None): #retrieve
	instance = get_object_or_404(Post, slug = slug)
	content = {
		"title" : instance.title,
		"instance" : instance,

	}
	return render(request, "post_detail.html", content)

@login_required(login_url='/login/')
def post_update(request, slug = None):
	instance = get_object_or_404(Post, slug = slug)
	form = PostForm(request.POST or None, request.FILES or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request, "Successfully Updated")
		return HttpResponseRedirect(instance.get_absolute_url())
	
	context = {
			"form" : instance.title,
			"instance" : instance,
			"form" : form,
			"type" : "Update",
	}
	return render(request, "post_form.html", context)


@login_required(login_url='/login/')
def post_delete(request, slug = None):
	instance = get_object_or_404(Post, slug = slug)
	instance.delete()
	messages.success(request, instance.title + " Successfully deleted")
	return redirect("posts:list")
