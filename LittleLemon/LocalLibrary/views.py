from django.shortcuts import render
from .models import Book, BookInstance, Author
from django.views import View
from django.views import generic
from pprint import pprint
from django.core.paginator import Paginator
from django.http import HttpRequest


def index(request: HttpRequest):
    """ Render the home page."""
    # Get visit count
    num_visits = request.session.get("num_visits", 0)
    num_visits += 1
    request.session["num_visits"] = num_visits
    
    # Counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    num_authors = Author.objects.count()    # all() implied by default
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }
    
    return render(request, 'LocalLibrary/index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    template_name = 'LocalLibrary/books/index.html'
    # context_object_name = 'book_list' : The view passes the context (list of books)
    # by default as object_list and book_list aliases; either will work.
    queryset = Book.objects.all()
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pprint(context)
        return context
    
    

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'LocalLibrary/books/book_detail.html'
    



class AuthorView(View):
    """Class to handle all requests associated with authors."""
    
    template = 'LocalLibrary/authors/index.html'
    def get(self, request, *args, **kwargs):
        authors = Author.objects.all()
        paginator  = Paginator(authors, 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj, 'author_list': page_obj.object_list}
        context['is_paginated'] = page_obj.has_other_pages()
        return render(request, self.template, context)
    
class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'LocalLibrary/authors/author_detail.html'