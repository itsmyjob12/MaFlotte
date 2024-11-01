# Generated by Django 3.2.6 on 2024-07-28 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_entretien'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carburant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=6)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='entretien',
            name='photo_entretien',
        ),
    ]
