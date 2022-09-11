from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Book
from django.db.models import Q, Sum


# Create your views here.


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/book_list.html'
    login_url = 'account_login'


class BookDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'books/book_detail.html'
    login_url = 'account_login'
    permission_required = 'books.special_status'


class SearchResultsListView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )


# count book sold by author and sort by highest
class AuthorListView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/author_list.html'

    def get_queryset(self):
        return Book.objects.values('author').annotate(
            copies_sold=Coalesce(Sum('copies_sold'), 0)
        ).order_by('-copies_sold')


class AuthorDetailView(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'books/author_detail.html'

    def get_object(self):
        return Book.objects.filter(author__id=self.kwargs['pk']).first()


class AuthorBookListView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/author_book_list.html'

    def get_queryset(self):
        return Book.objects.filter(author__id=self.kwargs['pk'])

