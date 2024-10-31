# Generated by Django 3.2.6 on 2024-07-28 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_conducteur_genre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entretien',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('date_entretien', models.DateField()),
                ('cout', models.DecimalField(decimal_places=2, max_digits=10)),
                ('photo_entretien', models.ImageField(blank=True, null=True, upload_to='entretiens/')),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('voiture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.voiture')),
            ],
        ),
    ]
