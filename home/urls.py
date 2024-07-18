from django.urls import path, re_path
from . import views
from .views import *

urlpatterns = [

    # The home page
    path('home/', views.index, name='home'),
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
    path('home/ajout/vehicule/', new_voiture, name='ajout_vehicule'),
    path('home/liste/vehicules/', list_voitures, name='liste_voiture'),
    path('home/ajout/conducteur/', new_conducteur, name='ajout_conducteur'),
    path('home/liste/conducteur/', list_conducteur, name='list_conducteur'),
    path('detail/conducteur/<int:conducteur_id>/', detail_conducteurs, name='detail_conducteur'),
    path('home/profile/', profile, name='profile'),
    path('detail/voiture/<int:voiture_id>/', detail_voiture, name='detail_voiture'),
    path('activate_conducteur/<int:user_id>/', activate_conducteur_role, name='activate_conducteur'),
    path('affect/voiture/<int:voiture_id>/', affect_voiture, name='affect_voiture'),
    

]
