from .models import Book, BookInstance, Author
from django.views import View
from django.views import generic
from pprint import pprint
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.contrib.auth.decorators import (
    login_required,
    permission_required
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
    )
from django.urls import reverse, reverse_lazy

from .forms import RenewBookForm
import datetime

@login_required
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


class BookListView(LoginRequiredMixin, generic.ListView):
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
    
    

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = 'LocalLibrary/books/book_detail.html'
    
       
    
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """ Generic class-based view listing books on loan to current user. """
    model = BookInstance
    template_name = 'LocalLibrary/bookinstances/bookinstance_list_borrowed_by_user.html'
    context_object_name = 'bookinstance_borrowed_list'
    
    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
        
    
class BooksOnLoanListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'LocalLibrary.can_mark_returned'
    model = BookInstance
    template_name = 'LocalLibrary/bookinstances/bookinstance_list_on_loan.html'
    context_object_name = 'bookinstance_on_loan_list'
    
    def get_queryset(self):
       return (
           BookInstance.objects.filter(status='o')
       )
       

@login_required
@permission_required('LocalLibrary.can_mark_returned')
def renew_book_librarian(request: HttpRequest, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)
    
    if request.method == 'POST':
        
        form = RenewBookForm(request.POST)
        
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            
            return redirect(reverse('LocalLibrary:all-borrowed'))
        
    else:
        proposed_renewal_date = (datetime.date.today() + datetime.timedelta(weeks=3)).strftime("%Y-%m-%d")
        form = RenewBookForm(initial={"renewal_date": proposed_renewal_date})
        
    context = {
        'form': form,
        'book_instance': book_instance
    }
    
    return render(request, 'LocalLibrary/bookinstances/book_renew_librarian.html', context)


class AuthorView(LoginRequiredMixin, View):
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
    
class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author
    template_name = 'LocalLibrary/authors/author_detail.html'
    
class AuthorCreateView(PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'LocalLibrary.add_author'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    # initial = {'date_of_death': '11/12/2022'}
    template_name = 'LocalLibrary/authors/author_form.html'
    
class AuthorUpdateView(PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'LocalLibrary.change_author'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name = 'LocalLibrary/authors/author_form.html'
    
class AuthorDeleteView(PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'LocalLibrary.delete_author'
    model = Author
    success_url = reverse_lazy('LocalLibrary:authors')
    template_name = 'LocalLibrary/authors/author_confirm_delete.html'
    
    def form_valid(self, form):
        try:
            self.object.delete()
            return redirect(self.success_url)
        except Exception as e:
            return redirect(reverse('LocalLibrary:author-delete', kwargs={'pk': self.object.pk}))