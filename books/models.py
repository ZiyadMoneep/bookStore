import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


# Create your models here.

# class Author(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=100)
#     phone = models.CharField(max_length=100)
#     book = models.ManyToManyField('Book', related_name='authors')
#
#     def __str__(self):
#         return self.name

class Book(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=250, blank=True)
    # author = models.CharField(max_length=100)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    isbn = models.CharField(max_length=13, blank=True)
    cover = models.ImageField(upload_to='covers/', blank=True)
    rating = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['id'], name='id_index'),
        ]
        permissions = [
            ('special_status', 'can read all books'),
        ]

    def __str__(self):
        return f"{self.title} - {self.author} - {self.price}"

    # def get_absolute_url(self):
    #     return reverse('book_detail', kwargs={'pk': str(self.pk)})
    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.id)])


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
