from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if email:
            email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    ROLE_NORMAL = 'normal'
    ROLE_CONDUCTEUR = 'Conducteur'
    ROLE_CHOICES = [
        (ROLE_NORMAL, 'Normal'),
        (ROLE_CONDUCTEUR, 'Conducteur'),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_NORMAL,
    )
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set', 
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        verbose_name=_('groups'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Change related_name to avoid conflict
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions'),
    )
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


# Create your models here.
def default_profile_image():
    return "images/profile/defaut1.png"

class Profile (models.Model):
        user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        profile_image = models.ImageField(upload_to='images/profile', blank=True  )
        role = models.IntegerField(choices=((1, 'Administrator'), (2, 'Conducteur'), ), default=1)
        # is_restreint = models.BooleanField(default= True)
        is_online = models.BooleanField(default=False)

        def __str__(self):
          return self.user.username


@receiver(post_save, sender=User)
def create_or_update_Conducteur_profile(sender, instance, created, **kwargs):
    if created and instance.groups.filter(name='Conducteur').exists():
        ConducteurProfile.objects.create(user=instance)
    elif instance.groups.filter(name='Conducteur').exists():
        instance.Conducteurprofile.save() 
   

# Create your models here
class ConducteurProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_new_conducteur = models.BooleanField(default=True)
    role = models.IntegerField(choices=((1, 'Administrator'), (2, 'Conducteur')), default=2)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)
    
    def __str__(self):
        return self.user.username
     #STANDARDS
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
 

#STANDARDS
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_new_admin = models.BooleanField(default=True)
    role = models.IntegerField(choices=((1, 'Administrator'), (2, 'Conducteur')), default=1)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)
    def __str__(self):
        return self.user.username

         #STANDARDS
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)