from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from authentication.models import User, Profile
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import MarqueVoiture, Modele, Conducteur, Voiture, Entretien, Carburant
import json
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from .models import Reparation
from django.views.decorators.http import require_POST
import datetime
from django.http import HttpResponseBadRequest


@login_required(login_url="/login/")
def index(request):
    

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


# @login_required(login_url="/login/")
# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:
#         load_template = request.path.split('/')[-1]

#         if load_template == 'admin':
#             return HttpResponseRedirect(reverse('admin:index'))
#         context['segment'] = load_template

#         html_template = loader.get_template('home/' + load_template)
#         return HttpResponse(html_template.render(context, request))

#     except template.TemplateDoesNotExist:

#         html_template = loader.get_template('home/page-404.html')
#         return HttpResponse(html_template.render(context, request))

#     except:
#         html_template = loader.get_template('home/page-500.html')
#         return HttpResponse(html_template.render(context, request))


def new_voiture(request):
    marques = MarqueVoiture.objects.all()
    modeles = Modele.objects.all()
    # Création d'un dictionnaire pour stocker les modèles de voitures
    # Ce dictionnaire sera renvoyé en JSON pour le filtrage des modèles selon la marque sélectionnée
    modeles_data = {}
    for modele in modeles:
        if modele.marque_id not in modeles_data:
            modeles_data[modele.marque_id] = []
        modeles_data[modele.marque_id].append({'id': modele.id, 'nom': modele.nom})

    if request.method == "POST":
        marque_voiture_id = request.POST.get("marque_voiture")
        modele_voiture_id = request.POST.get("modele")
        # Vérification des valeurs non vides
        if not marque_voiture_id:
            messages.error(request, "Veuillez sélectionner une marque de voiture.")
            return redirect('home/ajout/vehicule/')
        if not modele_voiture_id:
            messages.error(request, "Veuillez sélectionner un modèle de voiture.")
            return redirect('home/ajout/vehicule/')

        immatriculation = request.POST.get("immatriculation")
        numero_serie = request.POST.get("numero_serie")
        couleur_voiture = request.POST.get("couleur_voiture")
        photo_voiture = request.FILES.get("photo_voiture")
        annee_fabrication = request.POST.get("annee_fabrication")
        kilometrage = request.POST.get("kilometrage")
        type_carburant = request.POST.get("type_carburant")
        transmission = request.POST.get("transmission")
        codes_erreur = request.POST.get("codes_erreur")
        nombre_de_vitesse = request.POST.get("nombre_de_vitesse")

        try:
            marque_voiture_obj = MarqueVoiture.objects.get(pk=marque_voiture_id)
        except MarqueVoiture.DoesNotExist:
            messages.error(request, "La marque sélectionnée n'existe pas.")
            return redirect('home/ajout/vehicule/')
        try:
            modele_voiture_obj = Modele.objects.get(pk=modele_voiture_id)
        except Modele.DoesNotExist:
            messages.error(request, "Le modèle sélectionné n'existe pas.")
            return redirect('home/ajout/vehicule/')

        add_voiture = Voiture(
            modele=modele_voiture_obj,
            annee_fabrication=annee_fabrication,
            kilometrage=kilometrage,
            type_carburant=type_carburant,
            transmission=transmission,
            numero_serie=numero_serie,
            immatriculation=immatriculation,
            couleur_voiture=couleur_voiture,
            codes_erreur=codes_erreur,
            nombre_de_vitesse=nombre_de_vitesse,
            photo_voiture=photo_voiture,
        )

        if photo_voiture:
            add_voiture.photo_voiture = photo_voiture

        add_voiture.save()
        messages.success(request, f'Voiture {add_voiture.modele} a été bien ajoutée!')
        return redirect('liste_voiture')

    context = {
        'marques': marques,
        'modeles': modeles,
        # Envoi du dictionnaire en JSON
        'modeles_data': json.dumps(modeles_data),
        'segment': 'ajout_vehicule',
    }
    return render(request, 'home/Ajout-vehicule.html', context)




def edit_voiture(request, voiture_id):
    try:
        voiture = Voiture.objects.get(pk=voiture_id)
    except Voiture.DoesNotExist:
        messages.error(request, "La voiture sélectionnée n'existe pas.")
        return redirect('liste_voiture')

    marques = MarqueVoiture.objects.all()
    modeles = Modele.objects.all()
    modeles_data = {}
    for modele in modeles:
        if modele.marque_id not in modeles_data:
            modeles_data[modele.marque_id] = []
        modeles_data[modele.marque_id].append({'id': modele.id, 'nom': modele.nom})

    if request.method == "POST":
        voiture.marque_voiture_id = request.POST.get("marque_voiture")
        voiture.modele_id = request.POST.get("modele")
        voiture.immatriculation = request.POST.get("immatriculation")
        voiture.numero_serie = request.POST.get("numero_serie")
        voiture.couleur_voiture = request.POST.get("couleur_voiture")
        voiture.annee_fabrication = request.POST.get("annee_fabrication")
        voiture.kilometrage = request.POST.get("kilometrage")
        voiture.type_carburant = request.POST.get("type_carburant")
        voiture.transmission = request.POST.get("transmission")
        voiture.codes_erreur = request.POST.get("codes_erreur")
        voiture.numero_chassi = request.POST.get("numero_chassi")
        voiture.nombre_de_vitesse = request.POST.get("nombre_de_vitesse")
        photo_voiture = request.FILES.get("photo_voiture")
        
        if photo_voiture:
            voiture.photo_voiture = photo_voiture

        voiture.save()
        messages.success(request, f'Voiture {voiture.modele} a été mise à jour!')
        return redirect('liste_voiture')

    datas = {
        'marques': marques,
        'modeles': modeles,
        'modeles_data': json.dumps(modeles_data),
        'voiture': voiture,
    }
    return render(request, 'home/Edit-vehicule.html', datas)




def new_conducteur(request):
    context = {
        'segment': 'ajout_conducteur',
    }
    
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        adresse = request.POST.get('adresse')
        telephone = request.POST.get('telephone')
        site_web = request.POST.get('site_web')
        email = request.POST.get('email').strip()
        genre = request.POST.get('genre')
        photo_conducteur = request.FILES.get('photo_conducteur')

        # Valider les champs obligatoires
        if not name or not email:
            return HttpResponseBadRequest("Name and email are required.")

        # Créer un compte utilisateur pour le conducteur
        username = name.replace(' ', '_').lower()
        password = User.objects.make_random_password()
        user = User.objects.create_user(username=username, email=email, password=password)

        # Créer le conducteur
        new_conducteur = Conducteur.objects.create(
            name=name,
            adresse=adresse,
            telephone=telephone,
            site_web=site_web,
            email=email,
            photo_conducteur=photo_conducteur,
            genre=genre,
            user=user,
        )

        # Envoyer un e-mail avec les informations de connexion au conducteur
        subject = 'Your conducteur Account Password'
        login_url = request.build_absolute_uri(reverse('activate_conducteur', args=[user.id]))
        message = f'Dear {name},\n\nYour conducteur account has been created successfully. Your username is {username} and your password is {password}. You can log in to your account at {login_url}.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return redirect('list_conducteur')  # Rediriger vers une page appropriée après la création

    return render(request, 'home/Ajout-conducteur.html', context)


def activate_conducteur_role(request, user_id):
    if request.method == 'GET':
        try:
            user = get_user_model().objects.get(id=user_id)
            user.role = 'conducteur'
            user.save()
            return redirect('login_conducteur')  
        except get_user_model().DoesNotExist:
            return HttpResponseBadRequest("Invalid user ID")
    else:
        return HttpResponseBadRequest("Method not allowed")


#  liste des conducteurs
def list_conducteur(request):
    conducteurs = Conducteur.objects.all().order_by('-id')
    context = {
        'conducteurs': conducteurs,
        'segment': 'list_conducteur',
    }
    return render(request, 'home/liste-conducteur.html', context)



def list_voitures(request):
    voitures = Voiture.objects.all().order_by('-id')
    context = {
        'voitures': voitures,
        'segment': 'liste_voiture',
    }
    return render(request, 'home/liste-vehicule.html', context)


def delete_voiture(request, voiture_id):
    # Utilisez get_object_or_404 pour obtenir l'objet ou renvoyer une erreur 404 si non trouvé
    voiture = get_object_or_404(Voiture, id=voiture_id)

    if request.method == 'POST':
        voiture.delete()
        messages.success(request, "Voiture supprimée avec succès!")
        return redirect('liste_voiture')  # Assurez-vous que 'liste_voiture' est bien défini
    # Redirigez vers la liste des voitures pour les requêtes GET ou autres
    return redirect('liste_voiture')  


def detail_voiture(request, voiture_id):
    voitures = Voiture.objects.get(id=voiture_id)
    datas = {
        'voitures': voitures,
    }
    return render(request, 'home/vehicule.html', datas)


def detail_conducteurs(request, conducteur_id):
    conducteurs = Conducteur.objects.get(id=conducteur_id)
    datas = {
        'conducteurs': conducteurs,
    }
    return render(request, 'home/conducteur.html', datas)



@login_required
def profile(request):
    # Votre logique pour la vue profile
    return render(request, 'home/profile.html')


#  affecter une voiture à un conducteur 
def affect_voiture(request, voiture_id):
    voiture = get_object_or_404(Voiture, pk=voiture_id)
    conducteurs = Conducteur.objects.all()

    if request.method == 'POST':
        conducteur_id = request.POST.get('conducteur')
        try:
            conducteur = Conducteur.objects.get(pk=conducteur_id)
        except conducteur.DoesNotExist:
            messages.error(request, "Le conducteur sélectionné n'existe pas.")
            return redirect('affect_voiture', voiture_id=voiture_id)
    
     # Vérifiez si la voiture est déjà affectée à ce conducteur
        if voiture.conducteur_assigne == conducteur:
            messages.error(request, f"La voiture {voiture.modele} est déjà affectée au conducteur {conducteur.name}.")
            return redirect('affect_voiture', voiture_id=voiture_id)

        voiture.conducteur_assigne = conducteur
        voiture.statut = 'en attente de diagnostic'
        voiture.save()
        
        data = {
            'voiture': voiture,
            'conducteur': conducteur
        }
       
        # Envoyer un email au conducteur
        subject = 'Nouvelle voiture affectée pour diagnostic'
        message = f'Une nouvelle voiture a été affectée à votre conducteur pour diagnostic.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [conducteur.email]
        notice_html = render_to_string('home/emailAffect.html', data)
        send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=notice_html)

        messages.success(request, f'Voiture {voiture.modele} a été affectée au conducteur {conducteur.name}.')
        return redirect('home')
    
    contexts = {
        'voiture': voiture,
        'conducteurs': conducteurs
    }
    return render(request, 'home/affect_voiture.html', contexts)

def modify_conducteur(request, conducteur_id):
    conducteur = get_object_or_404(Conducteur, id=conducteur_id)
    
    if request.method == 'POST':
        name = request.POST.get('name', conducteur.name).strip()
        adresse = request.POST.get('adresse', conducteur.adresse)
        telephone = request.POST.get('telephone', conducteur.telephone)
        site_web = request.POST.get('site_web', conducteur.site_web)
        email = request.POST.get('email', conducteur.email).strip()
        photo_conducteur = request.FILES.get('photo_conducteur')

        # Valider les champs obligatoires
        if not name or not email:
            return HttpResponseBadRequest("Name and email are required.")

        # Mise à jour des attributs du conducteur
        conducteur.name = name
        conducteur.adresse = adresse
        conducteur.telephone = telephone
        conducteur.site_web = site_web
        conducteur.email = email
        if photo_conducteur:
            conducteur.photo_conducteur = photo_conducteur
        
        # Enregistrez les modifications dans la base de données
        conducteur.save()
        
        messages.success(request, "Conducteur modifié avec succès!")
        return redirect('list_conducteur')
    
    return render(request, 'home/modify_conducteur.html', {'conducteur': conducteur})

def delete_conducteur(request, conducteur_id):
    conducteur = get_object_or_404(Conducteur, id=conducteur_id)
    if request.method == 'POST':
        conducteur.delete()
        messages.success(request, "Conducteur supprimé avec succès!")
        return redirect('list_conducteur')
    return redirect('list_conducteur')


def maintenance(request):
    voitures = Voiture.objects.all()
    context = {
        'voitures': voitures,
        'segment': 'maintenance',
    }
    return render(request, 'home/maintenance.html', context)



def index(request):
    nombre_conducteur = Conducteur.objects.count()
    marques = MarqueVoiture.objects.all()
    nombre_Voiture = Voiture.objects.count()
    connected_profiles = Profile.objects.filter(is_online=True)
    nombre_profile = Profile.objects.count()
    
    context = {
        'nombre_conducteur': nombre_conducteur,
        'nombre_Voiture': nombre_Voiture,
        'nombre_profile': nombre_profile,
        'connected_profiles': connected_profiles,
        'segment': 'home',
        'marques': marques
    }
    
    return render(request, 'home/index.html', context)
    
def map_view(request):
    context = {
        'segment': 'map',
    }
    return render(request, 'home/map.html', context)

def profile(request):
    context = {
        'segment': 'profile',
    }
    return render(request, 'home/profile.html', context)

def carburant(request):
    context = {
        'segment': 'carburant',
    }
    return render(request, 'home/carburant.html', context)


def entretien(request):
    entretiens = Entretien.objects.all()  # Récupère tous les entretiens
    context = {
        'segment': 'entretien',
        'entretiens': entretiens,
    }
    return render(request, 'home/entretien.html', context)

def ajouter_entretien(request):
    if request.method == 'POST':
        voiture_id = request.POST.get('voiture')
        description = request.POST.get('description')
        date_entretien = request.POST.get('date_entretien')
        cout = request.POST.get('cout')
        photo_entretien = request.FILES.get('photo_entretien')

        try:
            voiture = Voiture.objects.get(id=voiture_id)
        except Voiture.DoesNotExist:
            print("Véhicule avec l'ID spécifié n'existe pas.")
            return redirect('entretien')  # Ou une autre gestion d'erreur appropriée

        Entretien.objects.create(
            voiture=voiture,
            description=description,
            date_entretien=date_entretien,
            cout=cout,
            photo_entretien=photo_entretien
        )
        return redirect('entretien')

    # Debug : Affiche le nombre de voitures récupérées
    voitures = Voiture.objects.all()
    print(f"Nombre de voitures récupérées : {voitures.count()}")

    return render(request, 'home/ajouter_entretien.html', {'voitures': voitures})


def liste_maintenances(request):
    maintenances = Reparation.objects.all()
    context = {
        'maintenances': maintenances,
        'segment': 'liste_maintenances',
    }
    return render(request, 'home/liste_maintenances.html', context)



@require_POST
def ajouter_reparation(request):
    voiture_id = request.POST.get('voiture')
    description = request.POST.get('description')
    date_reparation = request.POST.get('date_reparation')
    cout = request.POST.get('cout')

    # Vérification des champs requis
    if not all([voiture_id, description, date_reparation, cout]):
        return HttpResponseBadRequest("Tous les champs doivent être remplis.")

    # Vérification de l'existence de la voiture
    try:
        voiture = Voiture.objects.get(pk=voiture_id)
    except Voiture.DoesNotExist:
        return HttpResponseBadRequest("La voiture spécifiée n'existe pas.")

    # Vérification du format de la date
    try:
        date_reparation_obj = datetime.datetime.strptime(date_reparation, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponseBadRequest("Le format de la date est incorrect.")

    # Création de la réparation
    Reparation.objects.create(
        voiture=voiture,
        description=description,
        date_reparation=date_reparation_obj,
        cout=cout,
    )
    
    return redirect('maintenance')


def modifier_reparation(request, pk):
    reparation = get_object_or_404(Reparation, pk=pk)
    voitures = Voiture.objects.all()

    if request.method == 'POST':
        # Obtenez les nouvelles valeurs des champs depuis les données POST
        description = request.POST.get('description', reparation.description)
        date_reparation = request.POST.get('date_reparation', reparation.date_reparation)
        cout = request.POST.get('cout', reparation.cout)
        voiture_id = request.POST.get('voiture', reparation.voiture.id)

        # Vérifiez le format de la date
        try:
            date_reparation_obj = datetime.datetime.strptime(date_reparation, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Le format de la date est incorrect.'}, status=400)
        
        # Trouvez la voiture sélectionnée
        voiture = get_object_or_404(Voiture, pk=voiture_id)
        
        # Mettez à jour les champs
        reparation.description = description
        reparation.date_reparation = date_reparation_obj
        reparation.cout = cout
        reparation.voiture = voiture
        reparation.save()

        return redirect('liste_maintenances')

    # Si la méthode n'est pas POST, affichez le formulaire avec les données actuelles
    return render(request, 'home/edit_maintenance.html', {'reparation': reparation, 'voitures': voitures})
    
    # Si la méthode n'est pas POST, vous pouvez choisir de rendre un formulaire de modification


@require_POST
def supprimer_reparation(request, pk):
    reparation = get_object_or_404(Reparation, pk=pk)
    reparation.delete()
    return redirect('maintenance')


def gestion_carburant(request):
    carburant_entries = Carburant.objects.all()
    return render(request, 'carburant.html', {'carburant_entries': carburant_entries})

def add_carburant(request):
    if request.method == 'POST':
        form = CarburantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_carburant')
    else:
        form = CarburantForm()
    return render(request, 'carburant.html', {'form': form})

def modify_carburant(request, pk):
    entry = Carburant.objects.get(pk=pk)
    if request.method == 'POST':
        form = CarburantForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('gestion_carburant')
    else:
        form = CarburantForm(instance=entry)
    return render(request, 'carburant.html', {'form': form, 'entry': entry})

def delete_carburant(request, pk):
    entry = Carburant.objects.get(pk=pk)
    if request.method == 'POST':
        entry.delete()
        return redirect('gestion_carburant')
    return redirect('gestion_carburant')