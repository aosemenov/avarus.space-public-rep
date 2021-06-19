
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from datetime import date
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
# ПРОФИЛЬ
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    organization = models.CharField(max_length=200, blank=True, null=True)
    position = models.CharField(max_length=200, blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Book(models.Model):
    LOAN_STATUS = (
        ('pu', 'Public'),
        ('pr', 'Private')

    )
    title = models.CharField(max_length=200, blank=True, null=True)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, blank=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book", blank=True)
    specifications = models.FileField(upload_to='upload_datasets')
    dataset = models.CharField(max_length=200, blank=True, )
    dataset_env = models.CharField(blank=True, max_length=200)
    status = models.CharField(max_length=5, choices=LOAN_STATUS, blank=True, default='pr', help_text='Book availability')


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Dataset'

  # Required for unique book instances


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', blank=True, on_delete=models.PROTECT, null=True)
    LOAN_STATUS = (
        ('o', 'Available'),
        ('m', 'Wait')

    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ["book"]
        verbose_name = 'Dataset instance'

    def __str__(self):
        return '%s (%s)' % (self.id, self.book.title)


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '%s %s' % (self.last_name, self.first_name)


class FeedBack(models.Model):
    LOAN_STATUS = (
        ('o', 'Available'),
        ('m', 'Refused'),
        ('d', 'Waiting')

    )
    name = models.CharField('User name', max_length=120)
    name_space = models.CharField('Location', max_length=120)
    customer_login = models.CharField('Login user', max_length=120, blank=True, null=True)
    organization = models.CharField('Organization', max_length=120, null=True)
    position = models.CharField('Position', max_length=120, null=True)
    email = models.EmailField('Email', max_length=120, null=True, blank=True)
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='d', help_text='STATUS')
    description = models.CharField('Description', max_length=120, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Requests to access the dataset'


class AddLocations(models.Model):
    name = models.CharField('Location name', max_length=120, null=True)
    num = models.CharField('Number', max_length=120, null=True)
    authors = models.CharField('Authors', max_length=120, null=True)
    longitude = models.CharField('Longitude', max_length=120, null=True)
    latitude = models.CharField('Latitude', max_length=120, null=True)
    photo = models.FileField(upload_to='pictures', blank=True)
    url_photo = models.CharField('URL photo', max_length=120, null=True)
    url_page = models.CharField('URL page', max_length=120, null=True)
    plots = models.CharField('Number of plots', max_length=120, null=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Location'