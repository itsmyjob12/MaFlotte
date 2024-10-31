from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

    
# conducteur
class Conducteur(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    site_web = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    genre = models.CharField(max_length=10, choices=[('homme', 'Homme'), ('femme', 'Femme')])
    photo_conducteur = models.ImageField(upload_to='photo_conducteur/')
    status = models.BooleanField(default= True)
    date_add = models.DateTimeField(auto_now= True)
    date_update = models.DateTimeField(auto_now= True)
    
    def __str__(self) :
        return f"Nom du conducteur: {self.name}"    
    
    # marque de  la voiture
class MarqueVoiture(models.Model):
    marque = models.CharField(max_length=100)

    def __str__(self):
        return self.marque

# Modele de voiture
class Modele(models.Model):
    nom = models.CharField(max_length=100)
    marque = models.ForeignKey(MarqueVoiture, on_delete=models.CASCADE, related_name='modeles')

    def __str__(self):
        return f"{self.marque} {self.nom}"
    
     # standards
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)    


class Voiture(models.Model):
    modele = models.ForeignKey(Modele, on_delete=models.CASCADE)    
    TRANSMISSION_CHOICES = [
        ('Manuelle', 'Manuelle'),
        ('Automatique', 'Automatique'),
    ]
    TYPES_CARBURANT_CHOICES  = [
        ("Gasoil", "Gasoil"),
        ("Super", "Super"),
        ("Essence", "Essence"),
    ]
    STATUT_CHOICES = [
        ('en attente de diagnostic', 'En attente de diagnostic'),
        ('diagnostiquée', 'Diagnostiquee'),
    ]
    nombre_de_vitesse = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(10)])
    annee_fabrication = models.DateField()
    kilometrage = models.PositiveIntegerField()
    type_carburant = models.CharField(choices=TYPES_CARBURANT_CHOICES,max_length=50)
    transmission = models.CharField(max_length=50, choices=TRANSMISSION_CHOICES)
    numero_serie = models.CharField(max_length=100)
    immatriculation = models.CharField(max_length=20)
    symptomes = models.TextField()
    couleur_voiture = models.CharField(max_length=50)
    historique_maintenance = models.TextField()
    codes_erreur = models.TextField(blank=True, null=True)
    photo_voiture = models.ImageField(upload_to="voitures/")
    numero_chassi = models.CharField(max_length=50)
    statut = models.CharField(max_length=30, choices=STATUT_CHOICES, default='en attente de diagnostic')
    conducteur_assigne = models.ForeignKey(Conducteur, on_delete=models.SET_NULL, null=True, blank=True)

     # standards
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.modele.marque} {self.modele} - {self.annee_fabrication}"
    
class Reparation(models.Model):
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    description = models.TextField()
    date_reparation = models.DateField()
    cout = models.DecimalField(max_digits=10, decimal_places=2)
    photo_reparation = models.ImageField(upload_to='reparations/', blank=True, null=True)
    
    # standards
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Réparation pour {self.voiture} - {self.date_reparation}"    
    
class Entretien(models.Model):
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    description = models.TextField()
    date_entretien = models.DateField()
    cout = models.DecimalField(max_digits=10, decimal_places=2)
    
    # standards
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Entretien pour {self.voiture} - {self.date_entretien}"    
    
    
class Carburant(models.Model):
    vehicle = models.CharField(max_length=100)
    date = models.DateField()
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.vehicle} - {self.date}'    