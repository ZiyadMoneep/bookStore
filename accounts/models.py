from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum
from django.db.models.functions import Coalesce


# Create your models here.


class AuthorManager(models.Manager):
    def get_queryset(self):
        return AuthorQuerySet(self.model, using=self._db)

    def annotate_with_copies_sold(self):
        return self.get_queryset().annotate_with_copies_sold()


class AuthorQuerySet(models.QuerySet):
    def annotate_with_copies_sold(self):
        return self.annotate(copies_sold=Sum('books__copies_sold'))


class Author(AbstractUser):
    objects = AuthorManager()
    age = models.PositiveIntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name
