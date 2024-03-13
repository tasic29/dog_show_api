from django.conf import settings
from django.contrib import admin
from django.utils.text import slugify
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Owner(models.Model):
    phone = models.PositiveIntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    @admin.display(ordering='user__email')
    def email(self):
        return self.user.email

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'


class Breed(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Dog(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.IntegerField()
    weight = models.PositiveSmallIntegerField()
    color = models.CharField(max_length=255)
    owner = models.ForeignKey(
        Owner, on_delete=models.CASCADE, related_name='dogs')
    breed = models.ForeignKey(
        Breed, on_delete=models.CASCADE, related_name='dogs_breed')
    image = models.ImageField(
        upload_to='exibition/images', null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.name} - {self.breed}'


class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    contact_email = models.EmailField(unique=True)
    contact_phone = models.IntegerField()

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Show(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    sponsor = models.ForeignKey(
        Sponsor, on_delete=models.SET_NULL, null=True, related_name='shows')

    def __str__(self) -> str:
        return f'{self.name} - {self.location}'


class Judge(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.IntegerField()

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Vote(models.Model):
    dog = models.ForeignKey(
        Dog, on_delete=models.CASCADE, related_name='votes')
    point = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default=17)
