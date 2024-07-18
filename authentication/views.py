from django.shortcuts import render
import random
import string
import smtplib
from django.contrib import messages
from authentication.models import User
from django.contrib.auth import logout
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib.auth.models import  Group
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.decorators import login_required
from .forms import FirstLoginPasswordChangeForm 
from django.http import JsonResponse
from .forms import *  
from django.core.paginator import Paginator



def generate_random_password():
    # Génère un mot de passe aléatoire de 12 caractères
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(12))
    return password

def send_password_email(email, password):
    # Envoie l'email avec le mot de passe généré
    smtp_server = 'smtp.gmail.com'  # Remplacez par le serveur SMTP de votre fournisseur d'email
    smtp_port = 587  # Port SMTP
    smtp_username = 'traoremohamedjunior1234567899@gmail.com'  # Votre nom d'utilisateur SMTP
    smtp_password = 'qucseckyvffwuwad'  # Votre mot de passe SMTP

    from_email = 'admin@example.com'
    subject = 'Your Account Password'
    site_url = "http://127.0.0.1:8000/"
    message = f"Bienvenue ,\n\nThank you for choosing It Next. To proceed with your order, please confirm your email account by logging in.\n\nYour password is: {password}\n\nYou can log in here: {site_url}\n\nThank you,\nDonald\nProgrammeur"

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, email, f'Subject: {subject}\n\n{message}')
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

@login_required(login_url='login')
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        role = request.POST['role']
        
        if User.objects.filter(email=email):
            messages.error(request, 'This email is already associated with an account.')
            return redirect('register')
        
        if len(username) > 30:
            messages.error(request, 'Username must not be more than 30 characters.')
            return redirect('register')
        
        if User.objects.filter(username=username):
            messages.error(request, 'This username is already associated with an account.')
            return redirect('register')
        
        if len(firstname) > 30:
            messages.error(request, 'First name must not be more than 30 characters.')
            return redirect('register')
        
        if len(lastname) > 30:
            messages.error(request, 'Last name must not be more than 30 characters.')
            return redirect('register')

        # Générer un mot de passe aléatoire
        password = generate_random_password()

        # Envoyer le mot de passe par email
        send_password_email(email, password)

        my_user = User.objects.create_user(username=username, email=email, password=password)
        my_user.first_name = firstname
        my_user.last_name = lastname
        my_user.is_active = True
        my_user.save()

        if role == '1':
            # Créer un profil d'administrateur
            admin_profile = AdminProfile.objects.create(user=my_user)
            profile = Profile.objects.create(user=my_user, role=1) 
            profile.is_important = True
            my_user.is_superuser = True
            group, created = Group.objects.get_or_create(name='Admin')
            my_user.groups.add(group)
            my_user.save()
            admin_profile.save()
            profile.save()
        elif role == '2':
            conducteur_profile = ConducteurProfile.objects.create(user=my_user)
            profile = Profile.objects.create(user=my_user, role=2)  
            group, created = Group.objects.get_or_create(name='Conducteur')
            my_user.groups.add(group)
            conducteur_profile.save()
            profile.save()
            
        messages.success(request, 'The user account has been successfully created.')
        
        return redirect('home')

    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')
        
        # Rechercher l'utilisateur par email ou nom d'utilisateur
        user = User.objects.filter(Q(email=identifier) | Q(username=identifier)).first()

        if user is not None:
            authenticated_user = authenticate(request=request, username=user.username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
               
                if user.groups.filter(name='conducteur').exists():
                    if hasattr(user, 'ConducteurProfile') and user.ConducteurProfile.is_new_Conducteur:
                        return redirect('first_login_password_change')
                    else:
                        messages.success(request, 'Connexion réussie en tant que Conducteur')
                        return redirect('profile')  # Rediriger vers la page homeconducteur si l'utilisateur est un conducteur
                elif user.groups.filter(name='Admin').exists():                
                    if user.adminprofile.is_new_admin:
                        return redirect('first_login_password_change')
                    else:
                        messages.success(request, 'Connexion réussie')
                        return redirect('home') 
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Mauvaise authentification')
        else:
            messages.error(request, "Aucun utilisateur trouvé avec cet identifiant")

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    if request.user.is_authenticated:
        logout(request)
    messages.success(request, 'logout successfully!')
    return redirect('login')
 

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:

						return HttpResponse('Invalid header found.')
						
					messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
					return redirect ("password_reset_done2")
			messages.error(request, 'An invalid email has been entered.')
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password_reset2.html", context={"password_reset_form":password_reset_form})


@login_required
def first_login_password_change(request):
    user = request.user  # Assurez-vous que request.user est bien un objet User
    if request.method == 'POST':
        form = FirstLoginPasswordChangeForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()

                if hasattr(user, 'conducteurprofile') and user.conducteurprofile.is_new_Conducteur:
                    user.conducteurprofile.is_new_Conducteur = False
                    user.conducteurprofile.save()
                    return redirect('profile')
                elif hasattr(user, 'adminprofile') and user.adminprofile.is_new_admin:
                    user.adminprofile.is_new_admin = False
                    user.adminprofile.save()
                    return redirect('home')
            else:
                messages.error(request, "Passwords do not match.")
        else:
            messages.error(request, "Please correct errors in the form.")
    else:
        form = FirstLoginPasswordChangeForm()

    return render(request, 'accounts/first_login_password_change.html', {'form': form})
                

def password_change_view(request):
    from .forms import SignUpForm  # Importer à l'intérieur de la fonction
    msg = None
    success = False

    if request.method == "PUT":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get("role")

            if role == 'admin':
                admin_group, created = Group.objects.get_or_create(name='Administrateurs')
                admin_group.user_set.add(user)
            elif role == 'driver':
                driver_group, created = Group.objects.get_or_create(name='Conducteurs')
                driver_group.user_set.add(user)

            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect("/login/")
            else:
                msg = 'Authentication failed.'
        else:
            msg = 'Form is not valid: ' + str(form.errors)
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
