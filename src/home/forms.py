from django import forms


class FeedbackForm(forms.Form):
	email = forms.EmailField()
	message = forms.CharField(widget=forms.Textarea)