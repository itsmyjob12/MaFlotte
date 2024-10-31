from django.urls import path, re_path
from . import views
from .views import *

urlpatterns = [

    # The home page
    path('home/', views.index, name='home'),    
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
    path('home/ajout/vehicule/', new_voiture, name='ajout_vehicule'),
    path('edit/vehicule/<int:voiture_id>/', edit_voiture, name='edit_voiture'),
    path('delete/vehicule/<int:voiture_id>/', delete_voiture, name='delete_voiture'),
    path('home/liste/vehicules/', list_voitures, name='liste_voiture'),
    path('home/ajout/conducteur/', new_conducteur, name='ajout_conducteur'),
    path('home/liste/conducteur/', list_conducteur, name='list_conducteur'),
    path('detail/conducteur/<int:conducteur_id>/', detail_conducteurs, name='detail_conducteur'),
    path('home/profile/', profile, name='profile'),
    path('detail/voiture/<int:voiture_id>/', detail_voiture, name='detail_voiture'),
    path('activate_conducteur/<int:user_id>/', activate_conducteur_role, name='activate_conducteur'),
    path('affect/voiture/<int:voiture_id>/', affect_voiture, name='affect_voiture'),
    path('conducteur/modify/<int:conducteur_id>/', modify_conducteur, name='modify_conducteur'),
    path('conducteur/delete/<int:conducteur_id>/', delete_conducteur, name='delete_conducteur'),
    path('maintenance/', views.maintenance, name='maintenance'),
    path('liste-maintenance/', liste_maintenances, name='liste_maintenances'),
    path('ajouter-reparation/', ajouter_reparation, name='ajouter_reparation'),
    path('modifier-reparation/<int:pk>/', modifier_reparation, name='edit_maintenance'),
    path('supprimer-reparation/<int:pk>/', views.supprimer_reparation, name='delete_maintenance'),
    path('', views.index, name='index'),
    path('map/', views.map_view, name='map'),
    path('profile/', views.profile, name='profile'),
    path('carburant/', views.carburant, name='carburant'),
    path('entretien/', views.entretien, name='entretien'),
    path('ajouter_entretien/', views.ajouter_entretien, name='ajouter_entretien'),
    path('carburant/', views.gestion_carburant, name='gestion_carburant'),
    path('carburant/add/', views.add_carburant, name='add_carburant'),
    path('carburant/modify/<int:pk>/', views.modify_carburant, name='modify_carburant'),
    path('carburant/delete/<int:pk>/', views.delete_carburant, name='delete_carburant'),

]
