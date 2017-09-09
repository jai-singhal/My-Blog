from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import FeedbackForm

def feedback(request):
	form = FeedbackForm(request.POST or None)
	if form.is_valid():
		email = form.cleaned_data.get("email")
		message = form.cleaned_data.get("message")
		print(email, message)

		subject = "Hi There"
		msg = "ThankYou for the Feedback"
		from_email = settings.EMAIL_HOST_USER
		to_list = [email, "ironmist100@gmail.com"]

		send_mail(subject, msg, from_email, to_list, fail_silently = True)

		messages.success(request, "Message Successfully Sent")

	return render(request, "accounts_form.html", {
		"title" : "Feedback",
		"forms" : form,
	})