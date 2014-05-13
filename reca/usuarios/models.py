from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    Custom user class.
    """
    nombre = models.CharField(max_length=120, null=True)
    apellido_paterno = models.CharField(max_length=120, null=True)
    apellido_materno = models.CharField(max_length=120, null=True)
    email = models.EmailField(unique=True)
    fecha_de_nacimiento = models.DateField(blank=True, null=True)
    GENERO_CHOICES = (
        ('-','-'),
        ('M','Masculino'),
        ('F','Femenino'),
    )
    genero = models.CharField(max_length=1, blank=True, default='-', choices=GENERO_CHOICES)
    jefe = models.ForeignKey('User', editable=False, null=True)
    is_active = models.BooleanField(default=True, editable=False)
    is_admin = models.BooleanField(default=False, editable=False)
    is_staff = models.BooleanField(default=False, editable=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin       
