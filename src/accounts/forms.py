from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout,
	)
from django import forms

User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(
		widget = forms.PasswordInput,
	)

	def clean(self, *args, **keyargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		if username and password:
			user = authenticate(username = username, password = password)
			if not user:
				raise forms.ValidationError("This user does not exists")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect Password")
			if not user.is_active:
				raise forms.ValidationError("User is no longer active")		

		return super(UserLoginForm, self).clean(*args, **keyargs)





class UserRegisterForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			"username",
			"email",
			"email2", 
			"password",
		]
	
	email = forms.EmailField(label = "Email Address")
	email2 = forms.EmailField(label = "Confirm Email Address")
	password = forms.CharField(
		widget = forms.PasswordInput,
	)
	def clean(self, *args, **keyargs):
		email = self.cleaned_data.get("email")
		email2 = self.cleaned_data.get("email2")
		if email != email2:
			raise forms.ValidationError("Emails must match")
			return email
		
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("Email is already registered")

		return super(UserRegisterForm, self).clean(*args, **keyargs)


	# def clean_email2(self, *args, **keyargs):   for text box error
	# 	email = self.cleaned_data.get("email")
	# 	email2 = self.cleaned_data.get("email2")
	# 	if email != email2:
	# 		raise forms.ValidationError("Emails must match")
	# 		return email
		
	# 	email_qs = User.objects.filter(email=email)
	# 	if email_qs.exists():
	# 		raise forms.ValidationError("Email is already registered")

	# 	return super(UserRegisterForm, self).clean(*args, **keyargs)
