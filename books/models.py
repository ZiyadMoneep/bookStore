import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from accounts.models import Author


# Create your models here.

class Book(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=250, blank=True)
    copies_sold = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    isbn = models.CharField(max_length=13, blank=True)
    cover = models.ImageField(upload_to='covers/', blank=True)
    rating = models.IntegerField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['id'], name='id_index'),
        ]
        permissions = [
            ('special_status', 'can read all books'),
        ]

    def __str__(self):
        return f"{self.title} - {self.author} - {self.price}"

    def get_copies_sold(self):
        return self.copies_sold

    def get_author_name(self):
        return self.author.get_full_name()

    # def get_absolute_url(self):
    #     return reverse('book_detail', kwargs={'pk': str(self.pk)})
    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.id)])


class BookManager(models.Manager):
    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)

    def annotate_with_copies_sold(self):
        return self.get_queryset().annotate_with_copies_sold()


class BookQuerySet(models.QuerySet):
    def annotate_with_copies_sold(self):
        return self.annotate(copies_sold=Coalesce(Sum('books__copies_sold'), 0))


class Review(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    review = models.CharField(max_length=250)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.book} - {self.review} - {self.author}"
