from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from django.db.models.query_utils import Q
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm 
from .tokens import account_activation_token


def registerPage(request):
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():		
			user = form.save()
			user.is_active = False 
			user.save() 

			current_site = get_current_site(request)
			message = render_to_string('templates/users/acc_active_email.html', {
				'user':user, 
				'domain':current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			mail_subject = 'Activate your Virtual Tutoring App account.'
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
			
			messages.success(request, f'Please confirm your email address to complete the registration')
			return redirect('login')
	else:
		form = CreateUserForm()
	return render(request, 'templates/users/register.html', {'form': form})


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()

		messages.success(request, f'Thank you for your email confirmation. Now you can login your account.')
		return redirect('login')
	else:
		return HttpResponse('Activation link is invalid!')


def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'templates/users/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('home')


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					current_site = get_current_site(request)

					subject = "Password Reset Requested"
					email_template_name = "templates/users/password/password_reset_email.txt"
					c = {
							"email":user.email,
							'domain':current_site.domain,
							'site_name': 'Website',
							"uid": urlsafe_base64_encode(force_bytes(user.pk)),
							"user": user,
							'token': default_token_generator.make_token(user),
							'protocol': 'http',
						}
					email = render_to_string(email_template_name, c)
					try:
						email_test = EmailMessage(subject, email, to=[user.email])
						email_test.send()
						# send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect("/password_reset/done/")
	password_reset_form = PasswordResetForm()

	return render(request=request, template_name="templates/users/password/password_reset.html", context={"password_reset_form":password_reset_form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'templates/users/profile.html', context)