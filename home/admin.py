from django.contrib import admin
from .models import (Modele,MarqueVoiture,Voiture,Conducteur)

admin.site.register(Modele)
admin.site.register(MarqueVoiture)
admin.site.register(Voiture)
admin.site.register(Conducteur)