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
from django.contrib.auth import update_session_auth_hash




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
    message = f"Bienvenue ,\n\nMerci d'avoir. Pour continuer votre commande, veuillez confirmer votre compte e-mail en vous connectant.\n\nVotre mot de passe est: {password}\n\nVous pouvez vous connecter ici: {site_url}\n\nMerci,\nFleet\nManager"

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
            messages.error(request, 'Cet email est déjà associé à un compte.')
            return redirect('register')
        
        if len(username) > 30:
            messages.error(request, 'Le nom d_utilisateur ne doit pas dépasser 30 caractères.')
            return redirect('register')
        
        if User.objects.filter(username=username):
            messages.error(request, 'Ce nom d_utilisateur est déjà associé à un compte.')
            return redirect('register')
        
        if len(firstname) > 30:
            messages.error(request, 'Le prénom ne doit pas dépasser 30 caractères.')
            return redirect('register')
        
        if len(lastname) > 30:
            messages.error(request, 'Le nom de famille ne doit pas dépasser 30 caractères.')
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
            
        messages.success(request, 'Le compte utilisateur a été créé avec succès.')
        
        return redirect('home')

    return render(request, 'accounts/register.html')






def login_view(request):
    if request.method == "POST":
        identifier = request.POST['identifier']
        password = request.POST['password']
        
        # Rechercher l'utilisateur par email ou par nom d'utilisateur
        user = User.objects.filter(Q(email=identifier) | Q(username=identifier)).first()

        if user is not None:
            authenticated_user = authenticate(request=request, username=user.username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                try:
                    profile = user.profile
                    profile.is_online = True
                    profile.save()
                except Profile.DoesNotExist:
                    messages.error(request, 'Profil non trouvé.')
                # Vérifier si l'utilisateur a un ConducteurProfile
                try:
                    conducteur_profile = user.conducteurprofile
                    if conducteur_profile.is_new_conducteur:
                        return redirect('first_login_password_change')
                    else:
                        messages.success(request, 'Connexion réussie en tant que conducteur')
                        return redirect('profile')
                except ConducteurProfile.DoesNotExist:
                    # Vérifier si l'utilisateur a un AdminProfile
                    try:
                        admin_profile = user.adminprofile
                        if admin_profile.is_new_admin:
                            return redirect('first_login_password_change')
                        else:
                            messages.success(request, 'Connexion réussie')
                            return redirect('home')
                    except AdminProfile.DoesNotExist:
                        # Vérifier si l'utilisateur est un superutilisateur
                        if user.is_superuser:
                            messages.success(request, 'Connexion réussie en tant que superutilisateur')
                            return redirect('home')  # Redirige vers la page d'accueil pour les superutilisateurs
                        else:
                            messages.error(request, 'Profil non trouvé pour cet utilisateur')
                            return redirect('login')
            else:
                messages.error(request, 'Mauvaise authentification')
        else:
            messages.error(request, "Aucun utilisateur trouvé avec cet identifiant")

    return render(request, 'accounts/login.html')

def logout_view(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            profile.is_online = False
            profile.save()
        except Profile.DoesNotExist:
            messages.error(request, 'Profil non trouvé.')

    logout(request)
    messages.success(request, 'Déconnexion réussie!')
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
                update_session_auth_hash(request, user)  # Garder la session active après le changement de mot de passe
                
                # Mettre à jour le profil en fonction du type de profil
                if hasattr(user, 'conducteurprofile'):
                    user.conducteurprofile.is_new_conducteur = False
                    user.conducteurprofile.save()
                    return redirect('profile')
                elif hasattr(user, 'adminprofile'):
                    user.adminprofile.is_new_admin = False
                    user.adminprofile.save()
                    return redirect('home')
                return redirect('login')
            else:
                messages.error(request, "Les mots de passe ne correspondent pas.")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
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
