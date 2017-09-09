from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post
from django.utils import timezone

class PostForm(forms.ModelForm):
	title = forms.CharField()
	content = forms.CharField(
		widget = PagedownWidget(show_preview = False),
	    required = True,
	)
	class Meta:
		model = Post
		fields = [
			"title",
			"content",
			"image",
			"draft",
			"publish",
		]