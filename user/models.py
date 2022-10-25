from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from movie.models import Session


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('The Email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email=email, password=password, **extra_fields)


class SimpleUser(AbstractBaseUser):

    name = models.CharField(max_length=200, verbose_name='Імʼя')
    surname = models.CharField(max_length=200, verbose_name='Прізвище')
    alias = models.CharField(max_length=200, verbose_name='Псевдонім', unique=True)
    email = models.EmailField(max_length=200, verbose_name='E-mail', unique=True)
    password = models.CharField(max_length=200, verbose_name='Пароль', blank=True, null=True)  # delete blank and null
    card_number = models.CharField(max_length=16, verbose_name='Номер карти', blank=True, null=True)    # delete blank and null

    class Language(models.TextChoices):
        UKRAINIAN = 'ukrainian', 'Українська'
        RUSSIAN = 'russian', 'Російська'

    language = models.CharField(max_length=55, choices=Language.choices, verbose_name='Мова', default='ukrainian')

    class Sex(models.TextChoices):
        MALE = 'male', 'Чоловік'
        FEMALE = 'female', 'Жінка'

    sex = models.CharField(max_length=55, choices=Sex.choices, verbose_name='Стать', default='male')
    phone_number = PhoneNumberField()
    birthday = models.DateField(verbose_name='Дата народження')
    city = models.CharField(max_length=200, verbose_name='Місто')
    date_joined = models.DateTimeField(auto_now_add=True, blank=True, null=True)    # delete blank and null
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['alias', 'password']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, app_label):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True


class Ticket(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey(SimpleUser, on_delete=models.CASCADE)
    row_number = models.IntegerField(verbose_name='Номер ряду')
    seat_number = models.IntegerField(verbose_name='Номер місця')