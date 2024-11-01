# Generated by Django 3.2.6 on 2024-07-18 17:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='conducteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('adresse', models.CharField(max_length=100)),
                ('telephone', models.CharField(max_length=100)),
                ('site_web', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('photo_conducteur', models.ImageField(upload_to='photo_conducteur/')),
                ('status', models.BooleanField(default=True)),
                ('date_add', models.DateTimeField(auto_now=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MarqueVoiture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marque', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Modele',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('marque', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modeles', to='home.marquevoiture')),
            ],
        ),
        migrations.CreateModel(
            name='Voiture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_de_vitesse', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('annee_fabrication', models.DateField()),
                ('kilometrage', models.PositiveIntegerField()),
                ('type_carburant', models.CharField(choices=[('Gasoil', 'Gasoil'), ('Super', 'Super'), ('Essence', 'Essence')], max_length=50)),
                ('transmission', models.CharField(choices=[('Manuelle', 'Manuelle'), ('Automatique', 'Automatique')], max_length=50)),
                ('numero_serie', models.CharField(max_length=100)),
                ('immatriculation', models.CharField(max_length=20)),
                ('symptomes', models.TextField()),
                ('couleur_voiture', models.CharField(max_length=50)),
                ('historique_maintenance', models.TextField()),
                ('codes_erreur', models.TextField(blank=True, null=True)),
                ('photo_voiture', models.ImageField(upload_to='voitures/')),
                ('numero_chassi', models.CharField(max_length=50)),
                ('statut', models.CharField(choices=[('en attente de diagnostic', 'En attente de diagnostic'), ('diagnostiquée', 'Diagnostiquee')], default='en attente de diagnostic', max_length=30)),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('conducteur_assigne', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.conducteur')),
                ('modele', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.modele')),
            ],
        ),
    ]
