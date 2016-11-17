from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from models import Category, Page, UserProfile
from forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from datetime import datetime

def index(request):
		context_dict = {}
		#request.session.set_test_cookie()
		#if request.session.test_cookie_worked():
			#print ">>>> TEST COOKIE WORKED!"
			#request.session.delete_test_cookie()
		category_list = Category.objects.order_by('-likes')[:5]
		page_list = Page.objects.order_by('-views')[:5]
		context_dict = {'categories': category_list, 'pages': page_list}
		

		visits = request.session.get('visits')

		if not visits:
			visits = 1

		reset_last_visit_time = False
		
		#if 'last_visit' in request.COOKIES:
			#last_visit = request.COOKIES['last_visit']
		last_visit = request.session.get('last_visit')
		if last_visit:
				last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

				if (datetime.now() - last_visit_time).seconds > 0:
						visits = visits + 1
						reset_last_visit_time = True

		else:
				reset_last_visit_time = True
		
			
		if reset_last_visit_time:
			#response.set_cookie('last_visit', datetime.now())
			#response.set_cookie('visits', visits)
				request.session['last_visit'] = str(datetime.now())
				request.session['visits'] = visits

		context_dict['visits'] = visits
		response = render(request, 'index.html', context_dict)

		return response
	


def about(request):
	context_dict = {}
	if request.session.get('visits'):
			count = request.session.get('visits')
	else: 
		count = 0

	count = count + 1
	context_dict['visits'] = count
	
	return render(request, 'about.html', context_dict)

def category(request, category_name_slug):
		context_dict = {}
		try:
				category = Category.objects.get(slug=category_name_slug)
				pages = Page.objects.filter(category=category)

				context_dict['category'] = category
				context_dict['pages'] = pages

		except Category.DoesNotExist:
				pass

		return render(request, 'category.html', context_dict)

@login_required
def add_category(request):
		if request.method == 'POST':
				form = CategoryForm(request.POST)
				if form.is_valid():
						form.save(commit=True)
						return index(request)
				else:
						print form.errors
		else:
				form = CategoryForm()

		return render(request, 'add_category.html', {'form':form})
		# 
@login_required
def add_page(request, category_name_slug):
		try:

				cat = Category.objects.get(slug=category_name_slug)
		except Category.DoesNotExist:
				cat = None

		if request.method == 'POST':
				form =  PageForm(request.POST)

				if form.is_valid():
						if cat:
								page = form.save(commit=False)
								page.category = cat
								page.views = 0
								page.save()
								return category(request, category_name_slug)
						else:
								print form.errors
				else:
						print forms.errors
		else:
				form = PageForm()

		context_dict = {'form':form, 'category':cat, 'slug':category_name_slug}
		return render(request, 'add_page.html', context_dict)

def register(request):
		registered = False
		if request.method == 'POST':
				# Attempt to grab information from the raw form information.
				# Note that we make use of both UserForm and UserProfileForm.
				user_form = UserForm(data=request.POST)
				profile_form = UserProfileForm(data=request.POST)


				if user_form.is_valid() and profile_form.is_valid():
						# Save the user's form data to the database.
						user = user_form.save()

						# Now we hash the password with the set_password method.
						# Once hashed, we can update the user object.
						user.set_password(user.password)
						user.save()


						# Now sort out the UserProfile instance.
						# Since we need to set the user attribute ourselves, we set commit=False.
						# This delays saving the model until we're ready to avoid integrity problems.
						profile = profile_form.save(commit=False)
						profile.user = user

								# Did the user provide a profile picture?
								# If so, we need to get it from the input form and put it in the UserProfile model.
						if 'picture' in request.FILES:
								profile.picture = request.FILES['picture']

						# Now we save the UserProfile model instance.
						profile.save()

						# Update our variable to tell the template registration was successful.
						registered = True

				else:
						print user_form.errors, profile_form.errors

		else:
				user_form = UserForm()
				profile_form = UserProfileForm()

		return render(request,
				'register.html',
				{'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):
		if request.method == 'POST':
				username = request.POST.get('username')
				password = request.POST.get('password')

				user = authenticate(username=username, password=password)

				if user:

						if user.is_active:
								login(request, user)
								return HttpResponseRedirect('/')

						else:
								return HttpResponse("Your account is disabled.")
				else:
						print "Invalid login details: {0}, {1}".format(username, password)
						return HttpResponse("Invalid login details supplied.")

		else:
				return render(request, 'login.html', {})

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
		# Since we know the user is logged in, we can now just log them out.
		logout(request)

		# Take the user back to the homepage.
		return HttpResponseRedirect('/')

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
		# Since we know the user is logged in, we can now just log them out.
		logout(request)

		# Take the user back to the homepage.
		return HttpResponseRedirect('/')