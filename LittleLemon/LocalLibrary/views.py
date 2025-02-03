from django.shortcuts import render
from .models import Book, BookInstance, Author
from django.views import View


def index(request):
    """ Render the home page."""
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
    }
    
    return render(request, 'LocalLibrary/index.html', context=context)



class BookView(View):
    """Class to handle all requests associated with books."""
    
    template = 'LocalLibrary/books/index.html'
    
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        context = {'books': books}
        
        return render(request, BookView.template, context)