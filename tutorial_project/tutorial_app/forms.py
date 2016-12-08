from django import forms
from models import Page, Category, UserProfile
from django.contrib.auth.models import User  #add user profile
from django.core.mail import EmailMessage

class CategoryForm(forms.ModelForm):
		name = forms.CharField(max_length=128, help_text='Please enter a category name!')
		likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
		slug = forms.CharField(widget=forms.HiddenInput(), required=False)

		class Meta:
				model = Category
				fields = ('name',)
				exclude = ('user',)


class PageForm(forms.ModelForm):
		title = forms.CharField(max_length=128, help_text="Please eneter the title of the page.")
		url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
		views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

		def clean(self):
				cleaned_data = self.cleaned_data
				url = cleaned_data.get('url')

				if url and not url.startswith('http://'):
						url = 'http://'+ url
						cleaned_data['url'] = url
				return cleaned_data

		class Meta:
				model = Page
				exclude = ('category', 'user')

class UserForm(forms.ModelForm):
		password = forms.CharField(widget=forms.PasswordInput())

		class Meta:
				model = User
				fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
	
		class Meta:
				model = UserProfile
				fields = ('website', 'picture', 'bio')

class ContactForm(forms.Form):
	name = forms.CharField(required=True)
	email = forms.CharField(widget=forms.EmailInput(), required=True)
	subject = forms.CharField(required=True)
	body = forms.CharField(widget=forms.Textarea(), required=True)

	def send_message(self):
		name = self.cleaned_data['name']
		email = self.cleaned_data['email']
		subject = self.cleaned_data['subject']
		body = self.cleaned_data['body']

		message = '''
				New Message from {name} @ {email}
				Subject: {subject}
				Message:
				{body}
				'''.format(name=name, 
					email=email, 
					subject=subject, 
					body=body)

		email_msg = EmailMessage('New Contact Form Submission',
					message,
					email,
					['madelinegvera@gmail.com'])

		email_msg.send()
